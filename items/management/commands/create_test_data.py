from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from items.models import Item

class Command(BaseCommand):
    help = 'Creates test data'
    
    def handle(self, *args, **kwargs):
        User.objects.all().delete()
        
        # Создание пользователей
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_superuser': True,
                'is_staff': True
            }
        )
        admin.set_password('adminpass')
        admin.save()
        
        # Создаем обычных пользователей с правами доступа
        user1, created = User.objects.get_or_create(
            username='user1',
            defaults={
                'email': 'user1@example.com',
                'is_staff': True
            }
        )
        if created:
            user1.set_password('userpass')
            user1.save()
        
        user2, created = User.objects.get_or_create(
            username='user2',
            defaults={
                'email': 'user2@example.com',
                'is_staff': True
            }
        )
        if created:
            user2.set_password('userpass')
            user2.save()
        
        # Даем пользователям права на модель Item
        content_type = ContentType.objects.get_for_model(Item)
        permissions = Permission.objects.filter(content_type=content_type)
        
        for perm in permissions:
            user1.user_permissions.add(perm)
            user2.user_permissions.add(perm)
        
        # Создаем тестовые объекты Item
        Item.objects.get_or_create(
            name='Ноутбук',
            description='Мощный игровой ноутбук',
            owner=user1
        )
        Item.objects.get_or_create(
            name='Смартфон',
            description='Флагманский смартфон',
            owner=user1
        )
        Item.objects.get_or_create(
            name='Планшет',
            description='Графический планшет',
            owner=user2
        )
        
        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно созданы!'))