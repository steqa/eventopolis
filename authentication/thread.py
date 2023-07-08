import threading
import time

from django.core.mail import EmailMessage


class SendEmailThread(threading.Thread):
    def __init__(self, email: EmailMessage):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        time.sleep(0.001)
        self.email.send()
