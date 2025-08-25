/**
 * Main JavaScript file for ShalomGH Church Website
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initMobileMenu();
    initSmoothScrolling();
    initFormValidation();
    initLazyLoading();
    initAnimations();
    initLightbox();
});

/**
 * Mobile Menu Toggle - Simplified to avoid conflicts
 */
function initMobileMenu() {
    // Check if mobile menu is already initialized in header template
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    // Only initialize if elements exist and no existing handlers
    if (mobileMenuButton && mobileMenu && !mobileMenuButton.hasAttribute('data-initialized')) {
        console.log('Mobile menu already handled by header template');
        mobileMenuButton.setAttribute('data-initialized', 'true');
    }

/**
 * Accessible Lightbox for gallery images
 * Requires:
 *  - Triggers with class '.js-lightbox-trigger' and data-full, data-caption attributes
 *  - Modal container with id 'lightbox-modal'
 *  - Inside modal: #lightbox-image, #lightbox-caption, buttons #lightbox-prev, #lightbox-next
 *  - Any element with [data-lightbox-close] inside modal closes it
 */
function initLightbox() {
    const modal = document.getElementById('lightbox-modal');
    if (!modal) return; // only on pages that include the lightbox markup

    const triggers = Array.from(document.querySelectorAll('.js-lightbox-trigger'));
    if (!triggers.length) return;

    const img = document.getElementById('lightbox-image');
    const caption = document.getElementById('lightbox-caption');
    const btnPrev = document.getElementById('lightbox-prev');
    const btnNext = document.getElementById('lightbox-next');
    const closeEls = modal.querySelectorAll('[data-lightbox-close]');
    let index = 0;

    function open(i) {
        index = i;
        const t = triggers[index];
        if (!t) return;
        img.src = t.getAttribute('data-full');
        img.alt = t.getAttribute('data-caption') || '';
        caption.textContent = t.getAttribute('data-caption') || '';
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }
    function close() {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    }
    function next() { open((index + 1) % triggers.length); }
    function prev() { open((index - 1 + triggers.length) % triggers.length); }

    triggers.forEach((t, i) => {
        t.addEventListener('click', () => open(i));
        t.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                open(i);
            }
        });
    });
    closeEls.forEach(el => el.addEventListener('click', close));
    if (btnNext) btnNext.addEventListener('click', next);
    if (btnPrev) btnPrev.addEventListener('click', prev);
    document.addEventListener('keydown', (e) => {
        if (modal.classList.contains('hidden')) return;
        if (e.key === 'Escape') close();
        if (e.key === 'ArrowRight') next();
        if (e.key === 'ArrowLeft') prev();
    });
}
}

/**
 * Smooth Scrolling for Anchor Links
 */
function initSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Form Validation
 */
function initFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
        });
    });
}

function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    
    inputs.forEach(input => {
        if (!validateField(input)) {
            isValid = false;
        }
    });
    
    return isValid;
}

function validateField(field) {
    const value = field.value.trim();
    const type = field.type;
    let isValid = true;
    let message = '';
    
    // Remove existing error
    removeFieldError(field);
    
    // Required field validation
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        message = 'This field is required.';
    }
    
    // Email validation
    if (type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            message = 'Please enter a valid email address.';
        }
    }
    
    // Phone validation
    if (field.name === 'phone' && value) {
        const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
        if (!phoneRegex.test(value.replace(/[\s\-\(\)]/g, ''))) {
            isValid = false;
            message = 'Please enter a valid phone number.';
        }
    }
    
    if (!isValid) {
        showFieldError(field, message);
    }
    
    return isValid;
}

function showFieldError(field, message) {
    field.classList.add('border-red-500');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'text-red-500 text-sm mt-1';
    errorDiv.textContent = message;
    errorDiv.setAttribute('data-error-for', field.name);
    
    field.parentNode.appendChild(errorDiv);
}

function removeFieldError(field) {
    field.classList.remove('border-red-500');
    
    const existingError = field.parentNode.querySelector(`[data-error-for="${field.name}"]`);
    if (existingError) {
        existingError.remove();
    }
}

/**
 * Lazy Loading for Images
 */
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for older browsers
        images.forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('lazy');
        });
    }
}

/**
 * Scroll Animations
 */
function initAnimations() {
    const animatedElements = document.querySelectorAll('[data-animate]');
    
    if ('IntersectionObserver' in window) {
        const animationObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    const animation = element.dataset.animate;
                    element.classList.add(animation);
                }
            });
        }, {
            threshold: 0.1
        });
        
        animatedElements.forEach(el => animationObserver.observe(el));
    }
}

/**
 * Utility Functions
 */

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${getNotificationClass(type)}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

function getNotificationClass(type) {
    switch (type) {
        case 'success':
            return 'bg-green-500 text-white';
        case 'error':
            return 'bg-red-500 text-white';
        case 'warning':
            return 'bg-yellow-500 text-white';
        default:
            return 'bg-blue-500 text-white';
    }
}

// Format date
function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
