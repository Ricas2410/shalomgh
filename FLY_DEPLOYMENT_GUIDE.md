# 🚀 Fly.io Deployment Guide
## Seventh Day Sabbath Church Of Christ (ShalomGH)

### **Startup-Friendly Configuration**
- **App Name**: `shalomgh`
- **Domain**: `shalomgh.fly.dev`
- **Resources**: 512MB RAM, 1 CPU (shared)
- **Cost Optimization**: Auto-sleep, single machine
- **Database**: SQLite (no external DB costs)

---

## **📋 Pre-Deployment Checklist**

### **1. Install Fly.io CLI**
```bash
# Windows (PowerShell as Administrator)
iwr https://fly.io/install.ps1 -useb | iex

# macOS
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh
```

### **2. Create Fly.io Account**
1. Visit [fly.io](https://fly.io) and sign up
2. Add a payment method (required even for free tier)
3. Login via CLI: `flyctl auth login`

---

## **🚀 Deployment Steps**

### **Step 1: Set Production Secrets**
```bash
# Required secrets
flyctl secrets set SECRET_KEY="your-super-secret-production-key-here-make-it-long-and-random" --app shalomgh
flyctl secrets set ADMIN_EMAIL="admin@shalomgh.fly.dev" --app shalomgh
flyctl secrets set ALLOWED_HOSTS="shalomgh.fly.dev,*.fly.dev" --app shalomgh

# Church information
flyctl secrets set SITE_NAME="ShalomGH" --app shalomgh
flyctl secrets set CHURCH_NAME="Seventh Day Sabbath Church Of Christ" --app shalomgh

# Email configuration (optional but recommended)
flyctl secrets set EMAIL_HOST_USER="your-church-email@gmail.com" --app shalomgh
flyctl secrets set EMAIL_HOST_PASSWORD="your-gmail-app-password" --app shalomgh

# Social media (optional)
flyctl secrets set FACEBOOK_URL="https://facebook.com/shalomgh" --app shalomgh
flyctl secrets set TWITTER_URL="https://twitter.com/shalomgh" --app shalomgh
flyctl secrets set INSTAGRAM_URL="https://instagram.com/shalomgh" --app shalomgh
flyctl secrets set YOUTUBE_URL="https://youtube.com/@shalomgh" --app shalomgh

# SEO and Analytics (optional)
flyctl secrets set GOOGLE_ANALYTICS_ID="G-XXXXXXXXXX" --app shalomgh
flyctl secrets set GOOGLE_TAG_MANAGER_ID="GTM-XXXXXXX" --app shalomgh
```

### **Step 2: Deploy the Application**
```bash
# Navigate to your project directory
cd C:\Users\Deployment\Desktop\ShalomGH1

# Create the app (if not exists)
flyctl apps create shalomgh --org personal

# Create persistent volume for database
flyctl volumes create shalomgh_data --region iad --size 1 --app shalomgh

# Deploy
flyctl deploy --app shalomgh
```

### **Step 3: Verify Deployment**
```bash
# Check status
flyctl status --app shalomgh

# View logs
flyctl logs --app shalomgh

# Open in browser
flyctl open --app shalomgh
```

---

## **💰 Cost Optimization Features**

### **Auto-Sleep Configuration**
- **Automatic shutdown** when no traffic for 5 minutes
- **Instant wake-up** when someone visits
- **Zero cost** when sleeping
- **Minimal startup time** (~2-3 seconds)

### **Resource Limits**
- **512MB RAM**: Perfect for Django + SQLite
- **1 Shared CPU**: Adequate for church website traffic
- **1GB Storage**: Sufficient for media and database

### **Expected Monthly Cost**
- **Free tier**: Up to 160 hours/month (with auto-sleep)
- **Paid usage**: ~$1.94/month for 24/7 uptime
- **With auto-sleep**: Likely $0-5/month depending on traffic

---

## **🔧 Post-Deployment Configuration**

### **1. Create Superuser**
```bash
flyctl ssh console --app shalomgh
python manage.py createsuperuser
exit
```

### **2. Configure Admin Panel**
1. Visit `https://shalomgh.fly.dev/my-admin/`
2. Login with superuser credentials
3. Configure site settings:
   - Church name and contact info
   - Service times
   - Social media links
   - Hero section content

### **3. SEO Setup**
1. **Google Search Console**:
   - Add property: `https://shalomgh.fly.dev`
   - Verify ownership
   - Submit sitemap: `https://shalomgh.fly.dev/sitemap.xml`

2. **Google Analytics**:
   - Create GA4 property
   - Add tracking ID to secrets
   - Verify tracking

3. **Social Media**:
   - Test Open Graph: [Facebook Debugger](https://developers.facebook.com/tools/debug/)
   - Test Twitter Cards: [Twitter Card Validator](https://cards-dev.twitter.com/validator)

---

## **📊 Monitoring and Maintenance**

### **Useful Commands**
```bash
# View application logs
flyctl logs --app shalomgh

# SSH into the application
flyctl ssh console --app shalomgh

# Check application status
flyctl status --app shalomgh

# Scale down to save money (stops the app)
flyctl scale count 0 --app shalomgh

# Scale up to restart
flyctl scale count 1 --app shalomgh

# Update secrets
flyctl secrets set KEY=value --app shalomgh

# View current secrets
flyctl secrets list --app shalomgh
```

### **Performance Monitoring**
- **Response Time**: Monitor via Fly.io dashboard
- **Uptime**: Built-in health checks
- **Error Tracking**: Optional Sentry integration
- **Analytics**: Google Analytics for visitor insights

---

## **🛡️ Security Features**

### **Production Security**
- ✅ HTTPS enforced
- ✅ Security headers (HSTS, XSS protection)
- ✅ Secure cookies
- ✅ CSRF protection
- ✅ SQL injection protection
- ✅ Content Security Policy ready

### **Backup Strategy**
```bash
# Backup database (run monthly)
flyctl ssh console --app shalomgh
python manage.py dumpdata > backup_$(date +%Y%m%d).json
exit

# Download backup
flyctl ssh sftp get backup_YYYYMMDD.json --app shalomgh
```

---

## **🎯 Church-Specific Features**

### **SEO Optimization**
- ✅ Church-specific structured data
- ✅ Local SEO for Ghana
- ✅ Sabbath church keywords
- ✅ Founder recognition (Apostle Ephraim Kwaku Danso)
- ✅ Multiple church names (Shalom, Living Yahweh Sabbath Assemblies)

### **Content Management**
- ✅ Admin-manageable service times
- ✅ Sermon upload and management
- ✅ Event calendar
- ✅ Ministry directory
- ✅ Leadership profiles

---

## **🚨 Troubleshooting**

### **Common Issues**

**App won't start:**
```bash
flyctl logs --app shalomgh
# Check for missing secrets or configuration errors
```

**Database issues:**
```bash
flyctl ssh console --app shalomgh
python manage.py migrate
python manage.py collectstatic --noinput
```

**High costs:**
```bash
# Ensure auto-sleep is working
flyctl status --app shalomgh
# Should show "stopped" when no traffic
```

### **Support Resources**
- **Fly.io Docs**: [fly.io/docs](https://fly.io/docs)
- **Django Deployment**: [docs.djangoproject.com](https://docs.djangoproject.com/en/stable/howto/deployment/)
- **Community**: [community.fly.io](https://community.fly.io)

---

## **🎉 Success Checklist**

After deployment, verify:
- [ ] Website loads at `https://shalomgh.fly.dev`
- [ ] Admin panel accessible at `/my-admin/`
- [ ] Contact form works
- [ ] Service times page displays correctly
- [ ] All navigation links work
- [ ] Mobile responsiveness
- [ ] SEO meta tags present
- [ ] Google Analytics tracking (if configured)
- [ ] Auto-sleep working (check after 5 minutes of no traffic)

---

**Your Seventh Day Sabbath Church Of Christ website is now ready to serve your community with enterprise-level features at startup-friendly costs!** 🎉

**Domain**: https://shalomgh.fly.dev  
**Founded by**: Apostle Ephraim Kwaku Danso  
**Serving**: The global Sabbath church community
