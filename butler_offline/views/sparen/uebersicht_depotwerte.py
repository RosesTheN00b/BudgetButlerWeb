from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.converter import from_double_to_german


def _handle_request(request):
    depotwerte = persisted_state.database_instance().depotwerte
    if post_action_is(request, 'delete'):
        depotwerte.delete(int(request.values['delete_index']))
        return request_handler.create_redirect_context('/uebersicht_depotwerte/')

    db = depotwerte.get_all()
    depotwerte_liste = []
    for row_index, row in db.iterrows():
        depotwerte_liste.append({
            'index': row_index,
            'name': row.Name,
            'isin': row.ISIN,
            'wert': 'noch nicht ermittelt'
        })


    context = viewcore.generate_transactional_context('uebersicht_depotwerte')
    context['depotwerte'] = depotwerte_liste
    return context


def index(request):
    return request_handler.handle_request(request, _handle_request, 'sparen/uebersicht_depotwerte.html')

