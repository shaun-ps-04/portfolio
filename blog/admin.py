from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Post, Subscriber
from .send_mail import send_mail

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site


@admin.action(description='Send Post as Email to Confirmed Subscribers')
def send_post_email(post_admin, request, queryset):
    post = queryset[0]
    description = post.description[:300]

    current_site = get_current_site(request)
    confirmed_subs = Subscriber.objects.filter(confirmed=True)

    subject = 'New Post from Sean Stocker'

    for sub in confirmed_subs:
        html_content = render_to_string('blog/email/post_notification.html', {
            'user': sub,
            'domain': current_site.domain,
            'post_slug': post.slug,
            'title': post.title,
            'description': description,
        })
        send_mail(request, sub, html_content, subject)


class PostAdmin(admin.ModelAdmin):
    list_filter = ('published', 'created_at', 'updated_at',)
    list_display = ('title', 'published',)
    actions = [send_post_email]




admin.site.register(Post, PostAdmin)

class SubscriberAdmin(admin.ModelAdmin):
    list_filter = ('confirmed',)
    list_display = ('email', 'confirmed',)

admin.site.register(Subscriber, SubscriberAdmin)