#!/usr/bin/env python
"""
Quick diagnostic script for PythonAnywhere media upload issues
Run this on PythonAnywhere to diagnose upload problems
"""

import os
import sys
import django

# Setup Django
sys.path.append('/home/yourusername/BridesOfSaimaPortal')  # Update with your username
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BridesOfSaimaPortal.settings')
django.setup()

from django.conf import settings
from BridesOfSaima.models import Bride, BrideImage

def main():
    print("=" * 60)
    print("PythonAnywhere Media Upload Diagnostic")
    print("=" * 60)
    
    # 1. Check Django settings
    print(f"✓ MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"✓ MEDIA_URL: {settings.MEDIA_URL}")
    
    # 2. Check if directories exist
    media_root = str(settings.MEDIA_ROOT)
    brides_dir = os.path.join(media_root, 'brides')
    additional_dir = os.path.join(media_root, 'brides', 'additional')
    
    dirs_to_check = [media_root, brides_dir, additional_dir]
    
    for directory in dirs_to_check:
        if os.path.exists(directory):
            print(f"✅ Directory exists: {directory}")
            print(f"   Writable: {'Yes' if os.access(directory, os.W_OK) else 'No'}")
            print(f"   Permissions: {oct(os.stat(directory).st_mode)[-3:]}")
        else:
            print(f"❌ Directory missing: {directory}")
    
    # 3. Test write access
    print("\n" + "=" * 60)
    print("Testing Write Access")
    print("=" * 60)
    
    for directory in dirs_to_check:
        if os.path.exists(directory):
            test_file = os.path.join(directory, 'test_write_access.txt')
            try:
                with open(test_file, 'w') as f:
                    f.write('Test write access')
                
                with open(test_file, 'r') as f:
                    content = f.read()
                
                os.remove(test_file)
                print(f"✅ Write test passed: {directory}")
                
            except Exception as e:
                print(f"❌ Write test failed: {directory} - {e}")
        else:
            print(f"⚠️  Cannot test - directory doesn't exist: {directory}")
    
    # 4. Check database records vs files
    print("\n" + "=" * 60)
    print("Database vs Files Check")
    print("=" * 60)
    
    print(f"Total brides in database: {Bride.objects.count()}")
    print(f"Total additional images in database: {BrideImage.objects.count()}")
    
    missing_files = []
    
    # Check main images
    for bride in Bride.objects.all():
        if bride.image:
            file_path = os.path.join(media_root, str(bride.image))
            if os.path.exists(file_path):
                print(f"✅ Main image exists: {bride.image}")
            else:
                print(f"❌ Main image missing: {bride.image}")
                missing_files.append(str(bride.image))
    
    # Check additional images
    for img in BrideImage.objects.all():
        file_path = os.path.join(media_root, str(img.image))
        if os.path.exists(file_path):
            print(f"✅ Additional image exists: {img.image}")
        else:
            print(f"❌ Additional image missing: {img.image}")
            missing_files.append(str(img.image))
    
    # 5. Show file listing
    print("\n" + "=" * 60)
    print("Current Media Files")
    print("=" * 60)
    
    if os.path.exists(media_root):
        for root, dirs, files in os.walk(media_root):
            level = root.replace(media_root, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            
            sub_indent = ' ' * 2 * (level + 1)
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                print(f'{sub_indent}{file} ({file_size} bytes)')
    
    # 6. Summary and recommendations
    print("\n" + "=" * 60)
    print("Summary & Recommendations")
    print("=" * 60)
    
    if missing_files:
        print(f"❌ Found {len(missing_files)} missing files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\n💡 Recommendations:")
        print("1. Check if Django admin is saving files correctly")
        print("2. Run: python manage.py fix_pythonanywhere_uploads --fix-all")
        print("3. Check PythonAnywhere error logs")
        print("4. Verify static files mapping in Web tab")
    else:
        print("✅ All database records have corresponding files")
    
    print("\n🔧 Quick fixes to try:")
    print("1. Run the management command:")
    print("   python manage.py fix_pythonanywhere_uploads --fix-all")
    print("2. Check Web tab > Static files:")
    print("   URL: /media/")
    print(f"   Directory: {media_root}")
    print("3. Reload your web app after making changes")

if __name__ == "__main__":
    main()