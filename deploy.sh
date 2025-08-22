#!/bin/bash
# Deployment script for Seventh Day Sabbath Church Of Christ (ShalomGH) to Fly.io
# Startup-friendly configuration with cost optimization

echo "🚀 Deploying ShalomGH to Fly.io..."
echo "Church: Seventh Day Sabbath Church Of Christ"
echo "Founder: Apostle Ephraim Kwaku Danso"
echo "Domain: shalomgh.fly.dev"

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null; then
    echo "❌ flyctl is not installed. Please install it first:"
    echo "   Windows: iwr https://fly.io/install.ps1 -useb | iex"
    echo "   macOS: brew install flyctl"
    echo "   Linux: curl -L https://fly.io/install.sh | sh"
    exit 1
fi

# Login to Fly.io (if not already logged in)
echo "🔐 Checking Fly.io authentication..."
flyctl auth whoami || {
    echo "Please login to Fly.io:"
    flyctl auth login
}

# Create the app if it doesn't exist
echo "📱 Creating Fly.io app 'shalomgh'..."
flyctl apps create shalomgh --org personal 2>/dev/null || echo "App 'shalomgh' already exists"

# Create volume for persistent data (SQLite database)
echo "💾 Creating persistent volume..."
flyctl volumes create shalomgh_data --region iad --size 1 --app shalomgh 2>/dev/null || echo "Volume already exists"

# Set production environment secrets
echo "🔒 Setting production secrets..."
echo "Please set the following secrets manually using 'flyctl secrets set':"
echo ""
echo "Required secrets:"
echo "SECRET_KEY=your-super-secret-production-key-here"
echo "ADMIN_EMAIL=admin@shalomgh.fly.dev"
echo ""
echo "Optional secrets (for full functionality):"
echo "EMAIL_HOST_USER=your-church-email@gmail.com"
echo "EMAIL_HOST_PASSWORD=your-app-password"
echo "GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX"
echo "FACEBOOK_URL=https://facebook.com/shalomgh"
echo "TWITTER_URL=https://twitter.com/shalomgh"
echo "INSTAGRAM_URL=https://instagram.com/shalomgh"
echo "YOUTUBE_URL=https://youtube.com/@shalomgh"
echo ""
echo "Example command:"
echo "flyctl secrets set SECRET_KEY=your-secret-key-here --app shalomgh"
echo ""

read -p "Have you set the required secrets? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please set the secrets first, then run this script again."
    exit 1
fi

# Deploy the application
echo "🚀 Deploying to Fly.io..."
flyctl deploy --app shalomgh

# Check deployment status
echo "✅ Checking deployment status..."
flyctl status --app shalomgh

# Show the deployed URL
echo ""
echo "🎉 Deployment complete!"
echo "Your Seventh Day Sabbath Church Of Christ website is now live at:"
echo "https://shalomgh.fly.dev"
echo ""
echo "💰 Cost optimization features enabled:"
echo "- Auto-sleep when no traffic (saves money)"
echo "- 512MB RAM, 1 CPU (minimal resources)"
echo "- Single machine deployment"
echo "- SQLite database (no external DB costs)"
echo ""
echo "📊 Next steps:"
echo "1. Visit https://shalomgh.fly.dev to verify deployment"
echo "2. Set up Google Analytics and Search Console"
echo "3. Configure your social media links"
echo "4. Test all functionality"
echo ""
echo "🔧 Useful commands:"
echo "flyctl logs --app shalomgh          # View logs"
echo "flyctl ssh console --app shalomgh   # SSH into the app"
echo "flyctl status --app shalomgh        # Check status"
echo "flyctl scale count 0 --app shalomgh # Stop the app (save money)"
echo "flyctl scale count 1 --app shalomgh # Start the app"
