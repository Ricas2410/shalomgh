from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from typing import Optional
import io
import os
import logging
import base64
import requests


@deconstructible
class ImageKitStorage(Storage):
    """
    Minimal Django storage backend that uploads files to ImageKit.io and
    returns their CDN URLs for serving media.

    Notes:
    - Save returns the remote URL as the "name". Django can store full URLs
      for FileField/ImageField without issue.
    - delete/listdir/open are implemented minimally for compatibility.
    """

    def __init__(self, private_key: Optional[str] = None, public_key: Optional[str] = None, url_endpoint: Optional[str] = None):
        self.private_key = private_key or getattr(settings, 'IMAGEKIT_PRIVATE_KEY', '')
        self.public_key = public_key or getattr(settings, 'IMAGEKIT_PUBLIC_KEY', '')
        self.url_endpoint = url_endpoint or getattr(settings, 'IMAGEKIT_URL_ENDPOINT', '')

        if not (self.private_key and self.public_key and self.url_endpoint):
            raise ValueError("ImageKit credentials are not configured.")

        # Using REST API directly; no SDK client needed

    def _open(self, name, mode='rb'):
        # Remote readback is not supported; return an empty BytesIO to satisfy interface
        return io.BytesIO()

    def _save(self, name, content):
        # Ensure we can read bytes
        file_bytes = None
        if hasattr(content, 'file') and hasattr(content.file, 'read'):
            try:
                # Reset pointer if possible
                if hasattr(content.file, 'seek'):
                    content.file.seek(0)
            except Exception:
                pass
            file_bytes = content.file.read()
        else:
            try:
                if hasattr(content, 'seek'):
                    content.seek(0)
            except Exception:
                pass
            file_bytes = content.read()

        # Prefer direct REST API for reliability across SDK versions
        try:
            b64 = base64.b64encode(file_bytes).decode('ascii')
            safe_name = os.path.basename(name) or name or 'upload'
            folder = getattr(settings, 'IMAGEKIT_FOLDER', None)

            payload = {
                'file': b64,
                'fileName': safe_name,
            }
            if folder:
                payload['folder'] = folder

            resp = requests.post(
                'https://upload.imagekit.io/api/v1/files/upload',
                auth=(self.private_key, ''),
                data=payload,
                timeout=30,
            )
            resp.raise_for_status()
            result = resp.json()
        except Exception as e:
            raise IOError(f"ImageKit upload exception: {e}")

        def extract_url(obj):
            # Try dict-like
            if isinstance(obj, dict):
                u = obj.get('url')
                if u:
                    return u
                fp = obj.get('filePath') or obj.get('file_path')
                if fp:
                    endpoint = self.url_endpoint.rstrip('/')
                    return f"{endpoint}/{str(fp).lstrip('/')}"
                return None
            # Try attribute-style
            u = getattr(obj, 'url', None)
            if u:
                return u
            fp = getattr(obj, 'filePath', None) or getattr(obj, 'file_path', None)
            if fp:
                endpoint = self.url_endpoint.rstrip('/')
                return f"{endpoint}/{str(fp).lstrip('/')}"
            return None

        url = None

        # REST returns a dict
        url = extract_url(result)

        # Validate endpoint scheme if we had to build from filePath
        if url and not str(url).startswith('http'):
            if not (isinstance(self.url_endpoint, str) and self.url_endpoint.startswith('http')):
                raise IOError("ImageKit URL endpoint is invalid (must start with http/https)")
            # If still not absolute, compose
            url = f"{self.url_endpoint.rstrip('/')}/{str(url).lstrip('/')}"

        if not url:
            try:
                logging.getLogger(__name__).error(
                    "ImageKit upload missing URL. Result type=%s, dict_keys=%s",
                    type(result),
                    list(result.__dict__.keys()) if hasattr(result, '__dict__') else (list(result.keys()) if isinstance(result, dict) else None),
                )
            except Exception:
                pass
            raise IOError("ImageKit upload failed: missing URL in response")

        # Return the CDN URL as the stored name
        return url

    def exists(self, name):
        """Tell Django the name is available to avoid get_available_name loop.

        ImageKit uses unique file names by default, and we don't want Django to
        attempt to de-duplicate by probing existence.
        """
        return False

    def get_available_name(self, name, max_length=None):
        """Bypass Django's default de-duplication logic.

        We let ImageKit assign a unique name; we simply return the requested name.
        """
        return name

    def url(self, name):
        # If name is a full URL (starts with http), return as-is
        if isinstance(name, str) and name.startswith('http'):
            return name
        # Otherwise, construct using endpoint
        return f"{self.url_endpoint.rstrip('/')}/{name.lstrip('/')}"

    # Optional no-op implementations
    def delete(self, name):
        # You may implement deletion with fileId if needed.
        return

    def size(self, name):
        return None
