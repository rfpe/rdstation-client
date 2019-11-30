# encoding: utf-8
import os
import json
# import pprint
from rdstation_client import RDStationClient
from rdstation_client import ExceptionRDStationClient
from rdstation_client import ExceptionRDStationClientCreateCode
from rdstation_client import ExceptionRDStationClientResponse


def _create_rdc(file_auth='test_file_auth.json', console_input=False):
    if file_auth == 'test_file_auth.json':
        if os.path.exists(file_auth):
            os.unlink(file_auth)
    rdc = RDStationClient(file_auth, console_input=console_input, log=True)
    try:
        rdc._loading_params()
    except ExceptionRDStationClient:
        pass
    rdc._loading_params()
    return rdc


def test_exception_rdstation_client_response_1():
    obj = ExceptionRDStationClientResponse(json.dumps({
        'errors': {
            'api_identifier': [{
                'error_message': 'a field with '
                "'api_identifier' = "
                "'cf_my_custom_field' already "
                'exists',
                'error_type': 'TAKEN'}],
            'name': {'pt-BR': [{
                'error_message': "a field with 'name' = 'Meu "
                "campo customizado' already "
                'exists',
                'error_type': 'TAKEN'
            }]}}
    }))
    assert isinstance(
        obj.response_obj['errors']['api_identifier'][0]['error_message'],
        str
    )


def test_exception_rdstation_client_response_2():
    obj = ExceptionRDStationClientResponse(json.dumps({
        'errors': {
                'error_message': 'a field with '
                "'api_identifier' = "
                "'cf_my_custom_field' already "
                'exists',
                'error_type': 'TAKEN'}
    }))
    # pprint.pprint(str(obj))
    assert str(obj) == (
        'ExceptionRDStationClientResponse("a field with'
        ' \'api_identifier\' = \'cf_my_custom_field\' '
        'already exists", {\'errors\': {\'error_message'
        '\': "a field with \'api_identifier\' = "\n    '
        '                         "\'cf_my_custom_field'
        '\' already exists",\n'
        "            'error_type': 'TAKEN'}})"
    )
    assert isinstance(
        obj.response_obj['errors']['error_message'],
        str
    )


def test_exception_rdstation_client_response_3():
    obj = ExceptionRDStationClientResponse('Basic ERRORS')
    assert str(obj) == (
        'ExceptionRDStationClientResponse("Basic ERRORS", {})'
    )
    assert isinstance(obj.response_obj, dict)
    assert not bool(obj.response_obj)


def test__request():
    rdc = _create_rdc()
    rdc.client_id = None
    rdc._request(
        'get', 'https://httpstatuses.com/401'
    )
    assert bool(rdc.client_id)


def test__get_json_response_200s(mock_api):
    rdc = _create_rdc()
    respose = rdc._request(
        'get', 'https://httpstatuses.com/401'
    )
    try:
        rdc._get_json_response_200s(respose)
        raise Exception('not expected')
    except ExceptionRDStationClientResponse:
        pass


def test_not_file_auth():
    try:
        RDStationClient()
        raise Exception('not expected')
    except ExceptionRDStationClient:
        pass


def test_create_tokens_1():
    rdc = _create_rdc()
    rdc.access_token = None
    try:
        rdc.account_info_get()
        raise Exception('not expected')
    except ExceptionRDStationClientCreateCode:
        print(':)')


def test_create_tokens_2():
    rdc = _create_rdc()
    rdc.access_token = None
    rdc.refresh_token = None
    try:
        rdc.account_info_get()
        raise Exception('not expected')
    except ExceptionRDStationClientCreateCode:
        print(':)')


def test_account_info_get(mock_api):  # mock_api
    rdc = _create_rdc()  # 'rdstation_client.json'
    rdc.access_token = None
    rdc.refresh_token = None
    resp = rdc.account_info_get()
    assert bool(rdc.access_token)
    assert bool(rdc.refresh_token)
    assert isinstance(resp, dict)
    assert isinstance(resp['name'], str)


def test_tracking_code_get(mock_api):  # mock_api
    rdc = _create_rdc()  # 'rdstation_client.json'
    resp = rdc.tracking_code_get()
    assert isinstance(resp, dict)
    assert isinstance(resp['path'], str)


def test_contacts_get_by_uuid(mock_api):
    rdc = _create_rdc()  # 'rdstation_client.json'
    resp = rdc.contacts_get_by_uuid("b20da947-fbfd-4f0f-b338-fd08147d3842")
    assert isinstance(resp, dict)
    assert isinstance(resp['name'], str)


def test_contacts_get_by_email(mock_api):
    rdc = _create_rdc()  # 'rdstation_client.json'
    resp = rdc.contacts_get_by_email('sx.slex@gmail.com')
    assert isinstance(resp, dict)
    assert isinstance(resp['name'], str)
    resp = rdc.contacts_get_by_email('contact@example.com')
    assert isinstance(resp, dict)
    assert isinstance(resp['name'], str)


def test_contacts_patch(mock_api):
    rdc = _create_rdc()  # 'rdstation_client.json'
    resp = rdc.contacts_patch(
        {
            "name": "RD Station Developer",
            "email": "contact@example.com",
            "job_title": "Developer",
            "bio": "This documentation explains the RD Station API.",
            "website": "https://developers.rdstation.com/",
            "linkedin": "rd_station",
            "personal_phone": "+55 48 3037-3600",
            "city": "Florianópolis",
            "state": "SC",
            "country": "Brasil",
            "tags": ["developer", "rdstation", "api"]
        }
    )
    assert isinstance(resp, dict)
    assert isinstance(resp['name'], str)
    resp = rdc.contacts_patch(
        {
            "uuid": "b20da947-fbfd-4f0f-b338-fd08147d3842",
            "name": "RD Station Developer",
            "email": "contact@example.com",
            "job_title": "Developer",
            "bio": "This documentation explains the RD Station API.",
            "website": "https://developers.rdstation.com/",
            "linkedin": "rd_station",
            "personal_phone": "+55 48 3037-3600",
            "city": "Florianópolis",
            "state": "SC",
            "country": "Brasil",
            "tags": ["developer", "rdstation", "api"]
        }
    )
    assert isinstance(resp, dict)
    assert isinstance(resp['name'], str)


def test_fields_get(mock_api):  # mock_api
    rdc = _create_rdc()  # 'rdstation_client.json'
    resp = rdc.fields_get()
    assert isinstance(resp, dict)
    assert isinstance(resp['fields'], list)
    assert isinstance(resp['fields'][0]['uuid'], str)
    assert isinstance(resp['fields'][0]['api_identifier'], str)


def test_fields_post(mock_api):  # mock_api
    rdc = _create_rdc()  # 'rdstation_client.json'
    resp = rdc.fields_post(
        {
            "name": {
                "pt-BR": "Meu campo customizado"
            },
            "label": {
                "pt-BR": "Selecione uma das opções"
            },
            "api_identifier": "cf_my_custom_field",
            "data_type": "STRING",
            "presentation_type": "COMBO_BOX",
            "validation_rules": {
                "valid_options": [
                    {
                        "value": "opcao_1",
                        "label": {
                            "pt-BR": "opcao_1"
                        }
                    },
                    {
                        "value": "opcao_2",
                        "label": {
                            "pt-BR": "opcao_2"
                        }
                    }
                ]
            }
        }
    )
    assert isinstance(resp, dict)
    assert isinstance(resp['uuid'], str)


def test_fields_path(mock_api):
    rdc = _create_rdc()  # 'rdstation_client.json'
    resp = rdc.fields_path(
        {
            "uuid": "ca000da0-abc0-482a-935a-5bffab076d72",
            "name": {
                "pt-BR": "Meu campo customizado 2"
            }
        }
    )
    assert isinstance(resp, dict)
    assert isinstance(resp['uuid'], str)


def test_fields_delete(mock_api):  # mock_api
    rdc = _create_rdc()  # 'rdstation_client.json'
    resp = rdc.fields_delete(
        "4dda4645-6bc1-42aa-a1f6-60602369dd05"
    )
    assert isinstance(resp, dict)
    assert not bool(resp)


def test_events_post(mock_api):  # mock_api
    rdc = _create_rdc()  # 'rdstation_client.json'
    resp = rdc.events_post(
        {
            "event_type": "CONVERSION",
            "event_family": "CDP",
            "payload": {
                'conversion_identifier': 'registrou',
                'email': 'sx.slex+mayara+test4@gmail.com',
                'name': 'slex_test_mayara_test4'
            }
        }
    )
    assert isinstance(resp, dict)
    assert isinstance(resp['event_uuid'], str)

# # @requests_mock.mock()
# def test_contacts_patch(m):
#     # m.get('http://test.com', text='data')
#     resp = rdc.contacts_patch({
#         'email': 'sx.slex+991@gmail.com',
#         'name': 'Test991 SleX',
#         'tags': ['new-user']
#     })
#     assert isinstance(resp, dict)
#
#
# def test_events_post():
#     resp = rdc.events_post(
#         {
#             "event_type": "CONVERSION",
#             "event_family": "CDP",
#             "payload": {
#                 'conversion_identifier': 'test',
#                 'email': 'sx.slex+991@gmail.com'
#             }
#         }
#     )
#     assert resp.status_code == 200
#
#
# def test_contacts_get_by_email():
#     resp = rdc.contacts_get_by_email('sx.slex+991@gmail.com')
#     assert resp.status_code == 200

# def test_integrations_webhooks_get():
#     print(rdc)
#     # https://api.rd.services/integrations/webhooks