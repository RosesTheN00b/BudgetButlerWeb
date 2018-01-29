from viewcore import viewcore
from viewcore import request_handler
from viewcore import configuration_provider
def _handle_request(request):
    if request.method == 'POST' and request.POST['action'] == 'edit_databases':
        dbs = request.POST['dbs']
        configuration_provider.set_configuration('DATABASES', dbs)
        viewcore.DATABASES = []
        viewcore.DATABASE_INSTANCE = None

    if request.method == 'POST' and request.POST['action'] == 'add_kategorie':
        viewcore.database_instance().einzelbuchungen.add_kategorie(request.POST['neue_kategorie'])


    if request.method == 'POST' and request.POST['action'] == 'set_partnername':
        viewcore.database_instance().gemeinsamebuchungen.rename(viewcore.name_of_partner(), request.POST['partnername'])
        viewcore.save_refresh()
        configuration_provider.set_configuration('PARTNERNAME', request.POST['partnername'])

    context = viewcore.generate_base_context('configuration')
    default_databases = ''
    for db in viewcore.DATABASES:
        if len(default_databases) != 0:
            default_databases = default_databases + ','
        default_databases = default_databases + db
    context['default_databases'] = default_databases
    context['partnername'] = viewcore.name_of_partner()
    context['transaction_key'] = 'requested'
    return context

def index(request):
    return request_handler.handle_request(request, _handle_request, 'konfiguration.html')

