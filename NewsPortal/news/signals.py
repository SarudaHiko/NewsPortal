from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from news.models import Post
from news.utilits import mail_notify_new_post


@receiver(m2m_changed, sender=Post.category.through)
def notify_post_subscriber(sender, instance, **kwargs):
    # print('signal_job')
    if kwargs['action'] == 'post_add':
        new_post = Post.objects.get(pk=instance.pk)
        msg_data = {}
        msg_data['new_post_title'] = new_post.title
        msg_data['new_post_text'] = new_post.text[:63]
        msg_data['new_post_time'] = new_post.time
        msg_data['author_first_name'] = new_post.author.author_acc.first_name
        msg_data['author_last_name'] = new_post.author.author_acc.last_name
        msg_data['new_post_pk'] = new_post.id
        subscribers_name = new_post.category.values_list('subscribers__username', flat=True)
        for subscriber_name in subscribers_name:
            if subscriber_name:
                msg_data['subscriber_name'] = subscriber_name
                subscriber_email = User.objects.get(username=subscriber_name).email
                if subscriber_email:
                    msg_data['subscriber_email'] = subscriber_email
                    mail_notify_new_post(msg_data)
