import datetime

from django.shortcuts import render
from django.template.loader import render_to_string

from viewcore import viewcore
from viewcore import request_handler
from viewcore.converter import datum


def handle_request(request):
    if request.method == "POST" and request.POST['action'] == 'add':
        startdatum = request.POST['startdatum']
        startdatum = datetime.datetime.strptime(startdatum , '%d/%m/%Y')
        startdatum = startdatum.date()

        endedatum = request.POST['endedatum']
        endedatum = datetime.datetime.strptime(endedatum , '%d/%m/%Y')
        endedatum = endedatum.date()

        laenge = request.POST['laenge']
        laenge = datetime.datetime.strptime(laenge, '%H:%M').time()

        viewcore.database_instance().sollzeiten.add(startdatum, endedatum, laenge, "DATEV")
        viewcore.save_database()

    if request.method == "POST" and request.POST['action'] == 'edit':
        viewcore.database_instance().sollzeiten.edit(
            int(request.POST["edit_index"]),
            datum(request.POST['startdatum']),
            datum(request.POST['endedatum']),
            datetime.datetime.strptime(request.POST['laenge'], '%H:%M').time(),
            "DATEV")
        viewcore.save_database()

    soll_zeiten_liste = viewcore.database_instance().sollzeiten.get_sollzeiten_liste()
    for sollzeit in soll_zeiten_liste:
        sollzeit['Dauer'] = str(sollzeit['Dauer'])

    context = viewcore.generate_base_context("addsollzeit")
    context['ID'] = viewcore.get_next_transaction_id()
    context['arbeitgeber'] = viewcore.database_instance().get_arbeitgeber()
    context['alle_sollzeiten'] = soll_zeiten_liste
    return context

# Create your views here.
def index(request):
    return request_handler.handle_request(request, handle_request, 'theme/addsollzeit.html')

