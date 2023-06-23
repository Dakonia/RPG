from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Response
from django.conf import settings

@receiver(post_save, sender=Response)
def send_notification_email(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        author_email = post.author.email
        current_site = Site.objects.get_current()
        subject = 'Новый отклик на ваш пост'
        message = render_to_string(
            'email/notification_email.html',
            {'post': post, 'site': current_site}
        )
        plain_message = strip_tags(message)
        send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [author_email], html_message=message)



# @receiver(post_save, sender=Response)
# def send_notification_email(sender, instance, created, **kwargs):
#     if not created:
#         return
#
#     response = instance
#     post = response.post
#     author = post.author
#
#     if response.accepted:
#         subject = 'Ваш отклик принят'
#         message_template = 'email/accepted_response.html'
#     else:
#         subject = 'Ваш отклик отклонён'
#         message_template = 'email/rejected_response.html'
#
#     current_site = Site.objects.get_current()
#     message = render_to_string(message_template, {'response': response, 'site': current_site})
#     plain_message = strip_tags(message)
#     send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [author.email], html_message=message)
@receiver(post_save, sender=Response)
def send_notification_resp(sender, instance, created, **kwargs):
    if created:
        response = instance
        post = response.post
        print(post)
        author = post.author
        print(author)
        recipient_email = response.author.email
        print(recipient_email)
        current_site = Site.objects.get_current()
        print(current_site)

        if response.accepted:
            subject = 'Ваш отклик принят'
            template = 'email/accepted_response.html'
        else:
            subject = 'Ваш отклик отклонен'
            template = 'email/rejected_response.html'

        if response.accepted:  # Добавьте проверку значения поля accepted
            message = render_to_string(
                template,
                {'response': response, 'post': post, 'site': current_site}
            )
            print(message)
            plain_message = strip_tags(message)
            send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [recipient_email], html_message=message)