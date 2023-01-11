
from django.core.mail import send_mail, mail_admins
from django.shortcuts import render

def say_hello(request):
    send_mail('subject', 'messagee', 'info@moshbuy.com',['bob@moshbuy.com'])
    return render(request, 'hello.html', {'name':'mojtaba'})