from django.core.management.base import BaseCommand
from django.conf import settings
from BridesOfSaima.models import Bride, BrideImage
import os

class Command(BaseCommand):
    help = 'Fix bride image upload directories and check media files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-dirs',
            action='store_true',
            help='Create missing media directories',
        )
        parser.add_argument(
            '--check-files',
            action='store_true',
            help='Check if all database images have corresponding files',
        )
        parser.add_argument(
            '--fix-permissions',
            action='store_true',
            help='Fix directory permissions (Linux/Mac only)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Checking bride image configuration...'))
        
        # Check media root
        media_root = settings.MEDIA_ROOT
        self.stdout.write(f"Media root: {media_root}")
        
        if options['create_dirs']:
            self.create_directories()
        
        if options['check_files']:
            self.check_files()
            
        if options['fix_permissions']:
            self.fix_permissions()
        
        # Always show directory structure
        self.show_directory_structure()

    def create_directories(self):
        """Create necessary media directories"""
        self.stdout.write(self.style.WARNING('📁 Creating media directories...'))
        
        directories = [
            os.path.join(settings.MEDIA_ROOT, 'brides'),
            os.path.join(settings.MEDIA_ROOT, 'brides', 'additional'),
        ]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                self.stdout.write(self.style.SUCCESS(f"✅ Created directory: {directory}"))
            else:
                self.stdout.write(f"📁 Directory exists: {directory}")

    def check_files(self):
        """Check if database records have corresponding files"""
        self.stdout.write(self.style.WARNING('🔍 Checking database vs files...'))
        
        missing_files = []
        
        # Check main bride images
        for bride in Bride.objects.all():
            if bride.image:
                file_path = os.path.join(settings.MEDIA_ROOT, str(bride.image))
                if not os.path.exists(file_path):
                    missing_files.append(f"Main image: {bride.image} (Bride: {bride.name})")
                else:
                    self.stdout.write(f"✅ Found: {bride.image}")
        
        # Check additional images
        for bride_image in BrideImage.objects.all():
            file_path = os.path.join(settings.MEDIA_ROOT, str(bride_image.image))
            if not os.path.exists(file_path):
                missing_files.append(f"Additional image: {bride_image.image} (Bride: {bride_image.bride.name})")
            else:
                self.stdout.write(f"✅ Found: {bride_image.image}")
        
        if missing_files:
            self.stdout.write(self.style.ERROR('❌ Missing files:'))
            for file in missing_files:
                self.stdout.write(self.style.ERROR(f"  - {file}"))
        else:
            self.stdout.write(self.style.SUCCESS('✅ All database images have corresponding files'))

    def fix_permissions(self):
        """Fix directory permissions (Linux/Mac only)"""
        if os.name == 'nt':  # Windows
            self.stdout.write(self.style.WARNING('⚠️  Permission fixing not needed on Windows'))
            return
            
        self.stdout.write(self.style.WARNING('🔧 Fixing permissions...'))
        
        try:
            import stat
            media_root = settings.MEDIA_ROOT
            
            # Set directory permissions
            for root, dirs, files in os.walk(media_root):
                os.chmod(root, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)  # 755
                for file in files:
                    file_path = os.path.join(root, file)
                    os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)  # 644
            
            self.stdout.write(self.style.SUCCESS('✅ Permissions fixed'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error fixing permissions: {e}'))

    def show_directory_structure(self):
        """Show current media directory structure"""
        self.stdout.write(self.style.WARNING('📂 Current media directory structure:'))
        
        media_root = str(settings.MEDIA_ROOT)  # Convert to string
        if not os.path.exists(media_root):
            self.stdout.write(self.style.ERROR(f'❌ Media root does not exist: {media_root}'))
            return
        
        for root, dirs, files in os.walk(media_root):
            level = root.replace(media_root, '').count(os.sep)
            indent = ' ' * 2 * level
            self.stdout.write(f'{indent}{os.path.basename(root)}/')
            
            sub_indent = ' ' * 2 * (level + 1)
            for file in files:
                self.stdout.write(f'{sub_indent}{file}')