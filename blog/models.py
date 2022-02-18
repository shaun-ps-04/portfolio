from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

# 3rd Party
from tinymce import models as tinymce_models
from taggit.managers import TaggableManager

UserModel = get_user_model()


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(TimeStampMixin):
    title = models.CharField(max_length=128, blank=False, null=False, unique=True)
    slug = models.SlugField(blank=True, null=True)
    description = tinymce_models.HTMLField(blank=True, null=True)
    tags = TaggableManager()
    link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='uploaded', blank=True, null=True, default='default.png')
    published = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.image == '':  # Change image to default when image is deleted
            self.image = 'images/default.png'
        super(Post, self).save(*args, **kwargs)


class Subscriber(TimeStampMixin):
    email = models.EmailField(blank=False, null=False, unique=True)
    confirmed = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self):
        return self.email