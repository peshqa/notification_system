from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Item
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import F
from channels.layers import get_channel_layer

@receiver(pre_save, sender=Item)
def check_owner_change(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_owner = Item.objects.get(pk=instance.pk).owner
        except Item.DoesNotExist:
            instance._old_owner = None

@receiver(post_save, sender=Item)
def item_change_notification(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    
    if hasattr(instance, '_old_owner') and instance._old_owner:
        if instance._old_owner != instance.owner:
            
            async_to_sync(channel_layer.group_send)(
                f'user_{instance._old_owner.id}',
                {
                    'type': 'notify',
                    'message': f'Элемент "{instance.name}" передан другому пользователю'
                }
            )
            async_to_sync(channel_layer.group_send)(
                f'user_{instance.owner.id}',
                {
                    'type': 'notify',
                    'message': f'Вам передан элемент "{instance.name}"'
                }
            )
        else:
            if not created:
                message = f'Элемент "{instance.name}" был изменен'
                async_to_sync(channel_layer.group_send)(
                    f'user_{instance.owner.id}',
                    {
                        'type': 'notify',
                        'message': message
                    }
                )
    
