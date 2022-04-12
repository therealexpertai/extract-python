import unittest
import pytest
import time
from expertai.extract.extract_client import ExtractClient


class StatusTest(unittest.TestCase):
    def setUp(self):
        self.extract_client = ExtractClient(authorization_host="https://pe-nlapi-dev-developer.pe.cogitoapi.io/oauth2/token", host="https://pe-nlapi-dev-extract.pe.cogitoapi.io/beta")
        self.file_path = "../resources/test.pdf"
        self.file_name = 'test.pdf'
        self.task_response = None
        self.success_status_response = {'current': 100,
                                'message': 'completed',
                                'result': {'header': {'conversionDateTime': '2022-03-09 10:47',
                                                      'customInfo': {'Producer': 'Skia/PDF m100 Google Docs '
                                                                                 'Renderer',
                                                                     'Title': 'test'},
                                                      'documentName': 'test.pdf',
                                                      'errorPages': 0,
                                                      'metadata': [],
                                                      'totPages': 1,
                                                      'version': '2.1.1'},
                                           'layout': [{'bbox': [0, 0, 850, 1100],
                                                       'children': [2],
                                                       'id': 1,
                                                       'page': 1,
                                                       'type': 'page'},
                                                      {'bbox': [100, 100, 125, 114],
                                                       'content': 'test\n',
                                                       'id': 2,
                                                       'label': 'H',
                                                       'page': 1,
                                                       'parent': 1,
                                                       'type': 'text'}],
                                           'words': ['H4sIAK+FKGIC/ytJLS5hYGJgYEgB4lQgrgHiIiAGAEjL9hsZAAAA']},
                                'state': 'SUCCESS'}

    def test_layout_document_task_id_response(self):
        self.task_response = self.extract_client.layout_document_async(file_path=self.file_path,
                                                                       file_name=self.file_name)
        self.assertTrue(self.task_response['task_id'] is not None)

        if self.task_response is not None:
            self.check_status()

    def check_status(self):

        task_id = self.task_response['task_id']

        control_number = 0
        number = 10
        while self.status_state(task_id) != 'SUCCESS' and control_number < number:
            time.sleep(0.5)
            control_number += 0.5

        if control_number >= number:
            pytest.xfail('Can not get success response')

        status_response = self.extract_client.status(task_id)
        self.assertTrue(self.compare_responses(self.success_status_response, status_response))

    def status_state(self, task_id):
        result = self.extract_client.status(task_id)
        return result.get('state')

    def compare_responses(self, success_status_response, status_response):
        for key, value in success_status_response.items():
            if isinstance(value, dict):
                return self.compare_responses(value, status_response[key])
            elif isinstance(value, list):
                for el in value:
                    if isinstance(el, dict):
                        return self.compare_responses(el, status_response[key])
            elif key != 'conversionDateTime' and key != 'words' and key != 'Producer':
                if status_response[key] is None or status_response[key] != value:
                    return False

        return True
