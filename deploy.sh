#!/bin/bash

# Configuration
SERVER_USER="djwcixazph"
SERVER_HOST="server39.shared.spaceship.host"
DEST_PATH="~/dead-air-app/"

echo "🚀 Starting Deployment to Spaceship..."

# 1. Build the frontend
echo "📦 Building Frontend..."
cd frontend
npm install
npm run build
cd ..

# 2. Sync files to server
# We use rsync to only send changed files. 
# We exclude node_modules and other large/temporary folders.
echo "🔄 Syncing files to $SERVER_HOST..."
rsync -avz --exclude 'node_modules' \
          --exclude '.git' \
          --exclude 'frontend/node_modules' \
          --exclude 'backend/__pycache__' \
          --exclude '.env' \
          ./ $SERVER_USER@$SERVER_HOST:$DEST_PATH

# 3. Remote commands
echo "🔧 Setting up Remote Environment..."
ssh $SERVER_USER@$SERVER_HOST << EOF
    cd $DEST_PATH
    # Ensure backend directory exists
    cd backend
    # Re-install requirements if they changed (assuming a virtualenv is managed via cPanel)
    # pip install -r requirements.txt
    
    # Move frontend build to public directory if necessary
    # cp -r ../frontend/dist/* ~/public_html/
EOF

echo "✅ Deployment Complete!"
