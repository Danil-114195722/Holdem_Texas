from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class GameProfile(models.Model):
    user = models.OneToOneField(
        verbose_name=_('user email'),
        to=get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True
    )
    money = models.IntegerField(verbose_name=_('my money'), null=False, blank=False, default=100)
    win = models.IntegerField(verbose_name=_('my wins'), null=False, blank=False, default=0)
    defeat = models.IntegerField(verbose_name=_('my defeats'), null=False, blank=False, default=0)

    class Meta:
        verbose_name = _('game profile')
        verbose_name_plural = _('game profiles')


@receiver(models.signals.post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        GameProfile.objects.create(user=instance)


@receiver(models.signals.post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
