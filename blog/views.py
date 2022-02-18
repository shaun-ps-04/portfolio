from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Custom
from .models import Post, Subscriber
from .forms import PostForm, SubscriberForm

from .send_mail import send_mail
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token

# 3rd Party
from taggit.models import Tag


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title')
            post = Post.objects.get(title=title)
            messages.success(request, 'Post created!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()

    context = {'active': 'post_create', 'form': form}
    return render(request, 'blog/post_create.html', context)

@login_required
def post_edit(request, slug):
    post = Post.objects.get(slug=slug)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post edited!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)

    context = {'active': 'post_edit', 'form': form, 'post': post}
    return render(request, 'blog/post_edit.html', context)


def post_list(request):

    posts = Post.objects.filter(published=True).order_by('-created_at')

    post_title = request.GET.get('post-title')
    post_type = request.GET.get('post-type')
    post_count = request.GET.get('post-count')

    if post_title is not None:
        try:
            posts = posts.filter(title__icontains=post_title)
        except Exception as e:
            print(e)
    if post_type is not None:
        if post_type != 'empty':
            try:
                tag = Tag.objects.get(name=post_type)
                posts = posts.filter(tags=tag.id)
            except Exception as e:
                print(e)

    if post_count is not None:
        paginator = Paginator(posts, post_count)
    else:
        paginator = Paginator(posts, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    tags = Tag.objects.all()

    # Determine 'active' attribute
    if post_type is not None:
        active = str(post_type + 's')
    else:
        active = 'post_list'
        
    context = {'active': active, 'page_obj': page_obj, 'tags': tags}
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    post = None
    try:
        post = Post.objects.get(slug=slug)
    except Exception as e:
        print(e)
        messages.error(request, f'Post with slug "{slug}" does not exist.')
        return render(request, 'home.html', {})

    context = {'active': 'post_detail', 'post': post}
    return render(request, 'blog/post_detail.html', context)


def subscriber_view(request):
    
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        print('Request Method is POST')
        if form.is_valid():
            print('Is Valid? Yes')
            form.save()

            # Send email to subscriber to confirm account
            email = form.cleaned_data.get('email')
            sub = Subscriber.objects.get(email=email)
            if email is not None:
                sent = send_mail(request, sub)
                if sent:
                    messages.success(request, 'Almost there! A confirmation email has been sent to your account.')
                else:
                    messages.error(request, 'Error: Could not send email!')
            return redirect('home')
        else:
            email = request.POST.get('email')
            sub = Subscriber.objects.get(email=email)
            if sub.confirmed:
                messages.warning(request, 'This email is already subscribed')
                return redirect('home')
            if email is not None:
                sent = send_mail(request, sub)
                if sent:
                    messages.success(request, 'Almost there! A confirmation email has been sent to your account.')
                else:
                    messages.error(request, 'Error: Could not send email!')
            return redirect('home')

    else:
        form = SubscriberForm()

    context = {'active': 'post_subscribe', 'form': form}
    return render(request, 'blog/subscribe.html', context)


def sub_conf(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        sub = Subscriber.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Subscriber.DoesNotExist):
        sub = None

    if sub is not None and account_activation_token.check_token(sub, token):
        sub.confirmed = True
        sub.save()

        messages.success(request, 'Email has been verified!')
    else:
        messages.error(request, 'Activation link is invalid')

    return redirect('home')