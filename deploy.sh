#!/bin/bash
# Deployment script for PythonAnywhere
# Run this script after uploading files to PythonAnywhere

echo "🚀 Starting BridesOfSaima deployment on PythonAnywhere..."

# Navigate to project directory
cd ~/BridesOfSaimaPortal

# Create and activate virtual environment
echo "📦 Setting up virtual environment..."
python3.10 -m venv venv
source venv/bin/activate

# Install requirements
echo "📋 Installing requirements..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# Create media directory if it doesn't exist
mkdir -p media/brides media/brides/additional

echo "✅ Deployment setup complete!"
echo ""
echo "Next steps:"
echo "1. Go to PythonAnywhere Web tab"
echo "2. Create new web app (Manual configuration, Python 3.10)"
echo "3. Set source code: /home/yourusername/BridesOfSaimaPortal"
echo "4. Copy wsgi_config.py content to WSGI configuration"
echo "5. Add static file mappings:"
echo "   - /static/ → /home/yourusername/BridesOfSaimaPortal/staticfiles/"
echo "   - /media/ → /home/yourusername/BridesOfSaimaPortal/media/"
echo "6. Create superuser: python manage.py createsuperuser"
echo "7. Reload web app and test!"