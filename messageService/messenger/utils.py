from django.core.mail import send_mail
import datetime

def send_results(results):
    subject = 'Resumen de los Mensajes Enviados {}'.format(datetime.date.today())
    message = ' Este es el resumen de los mensajes enviados: {}'.format(results)
    email_from = ''
    recipient_list = ['']
    send_mail( subject, message, email_from, recipient_list )

    #amendez@ci3.es