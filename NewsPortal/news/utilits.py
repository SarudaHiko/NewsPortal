import datetime
import time

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPortal.settings import DEFAULT_FROM_EMAIL
from news.models import Post

DAY_POST_LIMIT = 3


def is_limit_spent(user):
    lim = DAY_POST_LIMIT
    quantity = Post.objects.filter(author__author_acc=user).count()
    if quantity < lim:
        return False
    else:
        time_post = Post.objects.filter(author__author_acc=user).order_by('-time').values_list('time', flat=True)[(lim-1):lim]
        dt = (time.time() - time_post[0].timestamp()) / 3600 / 24
        return (dt < 1)


def mail_notify_new_post(msg_data):
    html_content = render_to_string(
        'notify_new_post.html',
        {
            'msg_data': msg_data,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'Уведомление о новой публикации',
        body=f'Новая публикация в вашем любимом разделе',
        from_email=DEFAULT_FROM_EMAIL,
        to=[msg_data['subscriber_email'], ],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def weekly_notify_posts():
    last_week = datetime.datetime.now() - datetime.timedelta(days=7)
    users = User.objects.all()
    for user in users:
        msg_data = {}
        posts = Post.objects.filter(category__subscribers=user, time__gt=last_week).values('id').exists()
        if posts:
            msg_data['posts'] = Post.objects.filter(category__subscribers=user, id__gt=5).values('id', 'title', 'time')
            subscriber_email = user.email
            if subscriber_email:
                msg_data['subscriber_name'] = user.username
                msg_data['subscriber_email'] = subscriber_email
                mail_weekly_notify_posts(msg_data)


def mail_weekly_notify_posts(msg_data):
    html_content = render_to_string(
        'weekly_notify_posts.html',
        {
            'msg_data': msg_data,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'Публикации за неделю',
        body=f'Новые публикация в вашем любимом разделе',
        from_email=DEFAULT_FROM_EMAIL,
        to=[msg_data['subscriber_email'], ],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

