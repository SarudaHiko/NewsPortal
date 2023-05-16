from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import User, Post, Category
from celery import shared_task
from django.urls import reverse_lazy


@shared_task
def notify(post_id):
    post = Post.objects.get(id=post_id)
    categories = post.category.all()
    recipient_list = []
    for category in categories:
        subscribers = category.subscribers.all()
        recipient_list += [user.email for user in subscribers]

    if recipient_list:
        subject = f'Новый пост в категориях "{", ".join([str(category) for category in categories])}"'
        message = f'Появился новый пост в категориях "{", ".join([str(category) for category in categories])}"\n{post.content[:50]}'
        html = render_to_string('news_email.html', {'post': post})
        from_email = 'praviner@yandex.com'
        msg = EmailMultiAlternatives(subject, message, from_email, recipient_list)
        msg.attach_alternative(html, "text/html")
        msg.send()


@shared_task
def weekly_notify():
    from .views import mail_weekly_notify_posts_view
    recipient_list = User.objects.values_list('email', flat=True)

    if recipient_list:
        queryset = mail_weekly_notify_posts_view.get_queryset()
        if queryset.exists():
            subject = f'Еженедельный дайджест'
            message = f'Список новостей за прошедшую неделю'
            from_email = 'Pupapekainos@yandex.com'
            context = {'posts': queryset, 'request': None, 'filter': mail_weekly_notify_posts_view().filterset_class}
            html_content = render_to_string('weekly_posts_email.html', context)
            msg = EmailMultiAlternatives(subject, message, from_email, recipient_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
