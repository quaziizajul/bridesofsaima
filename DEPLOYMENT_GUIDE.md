# Deployment Checklist for PythonAnywhere

## Step 1: Prepare Your Local Project
- [x] Create requirements.txt file
- [x] Create production_settings.py file  
- [x] Create wsgi_config.py file
- [ ] Test locally with production settings

## Step 2: Upload Files to PythonAnywhere
1. Create a PythonAnywhere account (free tier available)
2. Go to Files tab in PythonAnywhere dashboard
3. Upload your project files or use git clone:
   ```bash
   git clone <your-repo-url> BridesOfSaimaPortal
   ```
   Or upload manually:
   - Upload the entire BridesOfSaimaPortal folder
   - Exclude: venv/, __pycache__/, *.pyc files

## Step 3: Create Virtual Environment on PythonAnywhere
1. Open a Bash console on PythonAnywhere
2. Navigate to your project:
   ```bash
   cd BridesOfSaimaPortal
   ```
3. Create virtual environment:
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```
4. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Step 4: Configure Database
1. Run migrations:
   ```bash
   python manage.py migrate
   ```
2. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```
3. Collect static files:
   ```bash
   python manage.py collectstatic --noinput
   ```

## Step 5: Configure Web App on PythonAnywhere
1. Go to Web tab in dashboard
2. Click "Add a new web app"
3. Choose "Manual configuration" (not Django wizard)
4. Select Python 3.10
5. Set source code directory: `/home/yourusername/BridesOfSaimaPortal`
6. Set working directory: `/home/yourusername/BridesOfSaimaPortal`
7. Edit WSGI configuration file and paste content from wsgi_config.py

## Step 6: Configure Static Files
In the Web tab, add static file mappings:
- URL: `/static/`
- Directory: `/home/yourusername/BridesOfSaimaPortal/staticfiles/`
- URL: `/media/`
- Directory: `/home/yourusername/BridesOfSaimaPortal/media/`

## Step 7: Update Settings
1. Edit production_settings.py and replace 'yourusername' with your actual PythonAnywhere username
2. Update ALLOWED_HOSTS with your actual domain: 'yourusername.pythonanywhere.com'
3. Set proper paths for STATIC_ROOT and MEDIA_ROOT

## Step 8: Test and Debug
1. Reload web app from Web tab
2. Visit your site: yourusername.pythonanywhere.com
3. Check error log if issues occur
4. Test all functionality: login, image upload, etc.

## Important Notes:
- Free PythonAnywhere accounts have limitations on outbound internet connections
- SQLite database works fine for small projects
- Keep your SECRET_KEY secure (use environment variables in production)
- Regularly backup your database and media files

## Troubleshooting:
- Check error logs in Web tab
- Ensure all file paths are correct
- Verify virtual environment is activated
- Check file permissions if needed