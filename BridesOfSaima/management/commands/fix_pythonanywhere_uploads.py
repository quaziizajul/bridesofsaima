from django.core.management.base import BaseCommand
from django.conf import settings
import os
import stat
import subprocess

class Command(BaseCommand):
    help = 'Fix PythonAnywhere media upload issues - creates directories and sets permissions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix-all',
            action='store_true',
            help='Fix all media upload issues',
        )
        parser.add_argument(
            '--create-dirs',
            action='store_true',
            help='Create media directories',
        )
        parser.add_argument(
            '--fix-permissions',
            action='store_true',
            help='Fix directory permissions',
        )
        parser.add_argument(
            '--check-disk-space',
            action='store_true',
            help='Check available disk space',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔧 PythonAnywhere Media Upload Fixer'))
        self.stdout.write(f"Media root: {settings.MEDIA_ROOT}")
        
        if options['fix_all']:
            self.create_directories()
            self.fix_permissions()
            self.check_disk_space()
            self.test_write_access()
        else:
            if options['create_dirs']:
                self.create_directories()
            if options['fix_permissions']:
                self.fix_permissions()
            if options['check_disk_space']:
                self.check_disk_space()

    def create_directories(self):
        """Create all required media directories"""
        self.stdout.write(self.style.WARNING('📁 Creating media directories...'))
        
        directories = [
            str(settings.MEDIA_ROOT),
            os.path.join(str(settings.MEDIA_ROOT), 'brides'),
            os.path.join(str(settings.MEDIA_ROOT), 'brides', 'additional'),
        ]
        
        for directory in directories:
            try:
                if not os.path.exists(directory):
                    os.makedirs(directory, mode=0o755, exist_ok=True)
                    self.stdout.write(self.style.SUCCESS(f"✅ Created: {directory}"))
                else:
                    self.stdout.write(f"📁 Exists: {directory}")
                    
                # Check if directory is writable
                if os.access(directory, os.W_OK):
                    self.stdout.write(f"✅ Writable: {directory}")
                else:
                    self.stdout.write(self.style.ERROR(f"❌ Not writable: {directory}"))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error creating {directory}: {e}"))

    def fix_permissions(self):
        """Fix directory permissions for PythonAnywhere"""
        self.stdout.write(self.style.WARNING('🔧 Fixing permissions...'))
        
        if os.name == 'nt':  # Windows
            self.stdout.write(self.style.WARNING('⚠️  Permission fixing not needed on Windows'))
            return
        
        directories = [
            str(settings.MEDIA_ROOT),
            os.path.join(str(settings.MEDIA_ROOT), 'brides'),
            os.path.join(str(settings.MEDIA_ROOT), 'brides', 'additional'),
        ]
        
        for directory in directories:
            if os.path.exists(directory):
                try:
                    # Set directory permissions to 755 (rwxr-xr-x)
                    os.chmod(directory, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
                    self.stdout.write(self.style.SUCCESS(f"✅ Fixed permissions: {directory}"))
                    
                    # Also fix permissions for any existing files
                    for root, dirs, files in os.walk(directory):
                        for file in files:
                            file_path = os.path.join(root, file)
                            try:
                                os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)  # 644
                            except Exception as e:
                                self.stdout.write(self.style.WARNING(f"⚠️  Could not fix file permissions for {file_path}: {e}"))
                                
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"❌ Error fixing permissions for {directory}: {e}"))

    def check_disk_space(self):
        """Check available disk space"""
        self.stdout.write(self.style.WARNING('💾 Checking disk space...'))
        
        try:
            if os.name != 'nt':  # Unix/Linux
                result = subprocess.run(['df', '-h', str(settings.MEDIA_ROOT)], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    self.stdout.write("Disk usage:")
                    self.stdout.write(result.stdout)
                else:
                    self.stdout.write(self.style.WARNING("Could not check disk space"))
            else:
                # Windows
                import shutil
                total, used, free = shutil.disk_usage(str(settings.MEDIA_ROOT))
                self.stdout.write(f"Free space: {free // (1024**3):.1f} GB")
                
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Could not check disk space: {e}"))

    def test_write_access(self):
        """Test if we can actually write files to the media directory"""
        self.stdout.write(self.style.WARNING('✍️  Testing write access...'))
        
        test_dirs = [
            os.path.join(str(settings.MEDIA_ROOT), 'brides'),
            os.path.join(str(settings.MEDIA_ROOT), 'brides', 'additional'),
        ]
        
        for test_dir in test_dirs:
            test_file = os.path.join(test_dir, 'test_write.txt')
            try:
                # Try to write a test file
                with open(test_file, 'w') as f:
                    f.write('Test file for write access')
                
                # Try to read it back
                with open(test_file, 'r') as f:
                    content = f.read()
                
                # Clean up
                os.remove(test_file)
                
                self.stdout.write(self.style.SUCCESS(f"✅ Write access OK: {test_dir}"))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Write access FAILED: {test_dir} - {e}"))
        
        self.stdout.write(self.style.SUCCESS('🎉 Media upload fix complete!'))
        self.stdout.write(self.style.WARNING('📝 Next steps:'))
        self.stdout.write('1. Reload your PythonAnywhere web app')
        self.stdout.write('2. Try uploading an image through Django admin')
        self.stdout.write('3. Check if the file appears in the media directory')