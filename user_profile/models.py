from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


DEFAULT_PROFILE_PHOTO = 'profile_photo/default_user_profile_photo.png'


class Profile(models.Model):
    user = models.OneToOneField(
        verbose_name=_('user email'),
        to=get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True
    )
    nickname = models.CharField(verbose_name=_('nickname'), max_length=50, null=True, blank=True)
    date_birth = models.DateField(verbose_name=_('birth date'), null=True, blank=True)
    location = models.CharField(verbose_name=_('location'), max_length=100, null=True, blank=True)
    bio = models.TextField(verbose_name=_('about you'), null=True, blank=True)
    photo = models.ImageField(
        verbose_name=_('profile photo'),
        null=True,
        blank=True,
        default=DEFAULT_PROFILE_PHOTO,
        upload_to='profile_photo/'
    )

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def about_you(self):
        """Return bio"""
        if self.bio:
            if len(self.bio) > 25:
                # return first 25 symbols of bio
                return f'{self.bio[:25]}...'
            return self.bio
        return

    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url

    def save(self, *args, **kwargs):
        # устанавливаем дефолтный ник, если он не задан
        if not self.nickname:
            user_id = get_user_model().objects.get(email=self.user).id
            self.nickname = _(f'User_{str(user_id).rjust(5, "0")}')

        # устанавливаем дефолтное фото, если оно было очищено
        if not self.photo:
            self.photo = DEFAULT_PROFILE_PHOTO

        super(Profile, self).save(*args, **kwargs)


@receiver(models.signals.post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(models.signals.post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
