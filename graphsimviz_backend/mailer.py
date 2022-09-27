from celery.utils.log import get_task_logger
from django.core.mail import send_mail

logger = get_task_logger(__name__)

# @shared_task
# def check_mails():
#     to_remove = set()
#     uids = set()
#     for n in Notification.objects.all():
#         if n.uid not in uids:
#             uids.add(n.uid)
#     for uid in uids:
#         t=Task.objects.get(uid= uid)
#         if t.sc_done:
#             to_remove.add(uid)
#             logger.info(f"Sending mails for task {uid}")
#             send_notification(uid)
#
# def get_notification_mails(id):
#     try:
#         mails = []
#         for n in Notification.objects.filter(uid=id):
#             mails.append(n.mail)
#         return mails
#     except Exception:
#         print("No mailing entries fround for ID="+id)
#         return None
#
#
# def send_notification(id):
#     mails = get_notification_mails(id)
#     if mails is not None:
#         link = "https://digest-validation.net/result?id="+id
#         send_mail('Your job has finished',f'The contribution signficance calculation for your digest-validation job has terminated.\nCheck them out here: {link}', 'info@digest-validation.net',mails, fail_silently=True)
#         remove_notification(id)
#
# def remove_notification(id):
#     for n in Notification.objects.filter(uid=id):
#         n.delete()

def error_notification(message):
    send_mail('Error in digest-execution',f'Message: {message}','info@digest-validation.net', ['status@andimajore.de'],True)

def server_startup():
    send_mail('GvL-Web system startup', f'The GvL backend is now ready!', 'info@digest-validation.net', ['status@andimajore.de'], fail_silently=False)
