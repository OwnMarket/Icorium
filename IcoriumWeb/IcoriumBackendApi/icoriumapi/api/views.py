import datetime
from django.core.mail import send_mail
from django.http import HttpResponse
from django.db import connection
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Quickview
from .models import IcoDetails
from .serializers import QuickviewSerializer
from .serializers import IcoDetailsSerializer
import pymssql


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def current_ico_list(request):
    if request.method == 'GET':
        company_name = request.GET.get('company', '')
        page = request.GET.get('page', '1')
        limit = request.GET.get('limit', '5')

        icos = Quickview.objects.raw("SELECT IcoId as id, IcoId as IcoId, IcoStart as IcoStart, Logo as Logo, CompanyName as CompanyName, OneLiner as OneLiner, WebsiteUrl as WebsiteUrl, IcoStatus as Status FROM SelectCurrentIcos(%s, %s, %s)", (company_name, page, limit))

        serializer = QuickviewSerializer(icos, many=True)
        return JSONResponse(serializer.data)

def upcoming_ico_list(request):
    if request.method == 'GET':
        company_name = request.GET.get('company', '')
        page = request.GET.get('page', '1')
        limit = request.GET.get('limit', '5')

        icos = Quickview.objects.raw("SELECT IcoId as id, IcoId as IcoId, IcoStart as IcoStart, Logo as Logo, CompanyName as CompanyName, OneLiner as OneLiner, WebsiteUrl as WebsiteUrl, IcoStatus as Status FROM SelectUpcomingIcos(%s, %s, %s)", (company_name, page, limit))

        serializer = QuickviewSerializer(icos, many=True)
        return JSONResponse(serializer.data)

def past_ico_list(request):
    if request.method == 'GET':
        company_name = request.GET.get('company', '')
        page = request.GET.get('page', '1')
        limit = request.GET.get('limit', '5')

        icos = Quickview.objects.raw("SELECT IcoId as id, IcoId as IcoId, IcoStart as IcoStart, Logo as Logo, CompanyName as CompanyName, OneLiner as OneLiner, WebsiteUrl as WebsiteUrl, IcoStatus as Status FROM SelectPastIcos(%s, %s, %s)", (company_name, page, limit))

        serializer = QuickviewSerializer(icos, many=True)
        return JSONResponse(serializer.data)

def ico_count(request):
    if request.method == 'GET':
        ico_total = '0'
        type = request.GET.get('type', '')
        company_name = request.GET.get('company', '')

        if (type == 'current'):
           ico_total = Quickview.objects.filter(IcoStart__lte=datetime.datetime.now(), IcoEnd__gte=datetime.datetime.now(), CompanyName__contains=company_name).count()
        elif (type == 'upcoming'):
           ico_total = Quickview.objects.filter(IcoStart__gt=datetime.datetime.now(), CompanyName__contains=company_name).count()
        elif (type == 'past'):
           ico_total = Quickview.objects.filter(IcoEnd__lt=datetime.datetime.now(), CompanyName__contains=company_name).count()

        data = {'TotalIcos': ico_total}
        return JSONResponse(data)

def ico_details(request):
    if request.method == 'GET':
        ico_id = request.GET.get('id', '0')

        icos = IcoDetails.objects.filter(IcoID__exact=ico_id)

        serializer = IcoDetailsSerializer(icos, many=True)
        return JSONResponse(serializer.data)

def company(request):
    if request.method == 'GET':
        companies = []
        icos = Quickview.objects.all().values('CompanyName')

        companies.append([company['CompanyName'] for company in icos])

        return JSONResponse(companies)

def send_contact_email(request):
    if request.method == 'GET':
        name = request.GET.get('name', '')
        email = request.GET.get('email', '')
        content = request.GET.get('content', '')
        
        if (email == ''):
            data = {'Success': False, 'Error': 'Email address is missing'}
        elif (content == ''):
            data = {'Success': False, 'Error': 'Message Content is missing'}
        else:
            try:
               send_mail(name + ' sent email from Icorium.io', content, email, ['contact@icorium.io'], fail_silently=False)
               data = {'Success': True}
            except BaseException as e:
               data = {'Success': False, 'Error': str(e)}
 
        return JSONResponse(data)
