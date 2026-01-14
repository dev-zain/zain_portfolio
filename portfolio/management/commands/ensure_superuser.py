from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates superuser if none exists'

    def handle(self, *args, **options):
        User = get_user_model()
        
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
            return
        
        User.objects.create_superuser(
            username='devzain',
            email='ibrahimkhan35821@gmail.com',
            password='zain35821'
        )
        self.stdout.write(self.style.SUCCESS('Superuser created: devzain'))
