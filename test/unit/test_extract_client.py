import unittest

from expertai.extract.extract_client import ExtractClient
from unittest.mock import patch


class ExtractClientTestCase(unittest.TestCase):
    def setUp(self):
        self.extract_client = ExtractClient(authorization_host="https://pe-nlapi-dev-developer.pe.cogitoapi.io/oauth2/token")
        self.file = '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'
        self.file_path = "../resources/test.pdf"
        self.file_name = 'test.pdf'
        self.task_id = 'test_id'
        self.response_with_layout_document = {'task_id': 'id'}
        self.response_with_task_id = {
            'current': 100,
            'message': 'completed',
            'result': {},
            'state': 'SUCCESS',
            'total': 100.0
        }

    @patch("expertai.extract.openapi.client.api.default_api.DefaultApi.layout_document_async_post", return_value={'task_id': 'id'})
    def test_layout_document_async_called_with_file(self, patch_layout_document_async_post):
        response = self.extract_client.layout_document_async(file=self.file, file_name=self.file_name)
        self.assertEqual(self.response_with_layout_document, response)

    @patch("expertai.extract.openapi.client.api.default_api.DefaultApi.layout_document_async_post", return_value={'task_id': 'id'})
    def test_layout_document_async_called_with_file_path(self, patch_layout_document_async_post):
        response = self.extract_client.layout_document_async(file_path=self.file_path, file_name=self.file_name)
        self.assertEqual(self.response_with_layout_document, response)

    @patch("expertai.extract.openapi.client.model.layout_request.LayoutRequest")
    @patch("expertai.extract.openapi.client.api.default_api.DefaultApi.layout_document_async_post")
    def test_layout_document_async_called_api_instance(self, patch_layout_document_async_post, patch_layout_request):
        with self.extract_client.layout_document_async(file=self.file, file_name=self.file_name):
            arg = patch_layout_document_async_post.call_args_list[0][1]
            layout_object = patch_layout_request(arg.get('layout_request'))

            request = patch_layout_request({"name": self.file_name, "data": self.file})

            self.assertEqual(layout_object, request)

    @patch("expertai.extract.openapi.client.api.default_api.DefaultApi.layout_document_async_post")
    def test_layout_document_async_called_once_api_instance(self, patch_layout_document_async_post):
        with self.extract_client.layout_document_async(file=self.file, file_name=self.file_name):
            patch_layout_document_async_post.assert_called_once()

    def test_layout_document_async_with_wrong_base64_file(self):
        with self.assertRaises(Exception) as context:
            self.extract_client.layout_document_async(file='test')

        self.assertTrue("Not correct configurations" in str(context.exception))

    def test_layout_document_async_with_file_without_file_name(self):
        with self.assertRaises(Exception) as context:
            self.extract_client.layout_document_async(file=self.file)

        self.assertTrue("Not correct configurations" in str(context.exception))

    def test_layout_document_async_without_file_and_file_path(self):
        with self.assertRaises(Exception) as context:
            self.extract_client.layout_document_async(file_name=self.file_name)

        self.assertTrue("Not correct configurations" in str(context.exception))

    def test_layout_document_async_with_file_path_without_file_name(self):
        with self.assertRaises(Exception) as context:
            self.extract_client.layout_document_async(file_path=self.file_path)

        self.assertTrue("Not correct configurations" in str(context.exception))

    def test_layout_document_async_without_parameters(self):
        with self.assertRaises(Exception) as context:
            self.extract_client.layout_document_async()

        self.assertTrue("Not correct configurations" in str(context.exception))

    def test_layout_document_async_with_file_and_file_path(self):
        with self.assertRaises(Exception) as context:
            self.extract_client.layout_document_async(file=self.file, file_path=self.file_path)

        self.assertTrue("Not correct configurations" in str(context.exception))

    def test_layout_document_async_with_file_file_path_and_file_name(self):
        with self.assertRaises(Exception) as context:
            self.extract_client.layout_document_async(file=self.file, file_path=self.file_path, file_name=self.file_name)

        self.assertTrue("Not correct configurations" in str(context.exception))

    def test_layout_document_async_with_wrong_path(self):
        wrong_path = "../resources/dont_exist.pdf"
        with self.assertRaises(Exception) as context:
            self.extract_client.layout_document_async(file_path=wrong_path, file_name="dont_exist.pdf")

        self.assertTrue("Not correct file_path" in str(context.exception))

    @patch("expertai.extract.openapi.client.api.default_api.DefaultApi.status_task_id_get")
    def test_status_called_api_instance(self, patch_status_task_id_get):
        with self.extract_client.status(self.task_id):
            patch_status_task_id_get.assert_called_with(task_id=self.task_id)

    @patch("expertai.extract.openapi.client.api.default_api.DefaultApi.status_task_id_get")
    def test_status_called_once_api_instance(self, patch_status_task_id_get):
        with self.extract_client.status(self.task_id):
            patch_status_task_id_get.assert_called_once()

    @patch(
        "expertai.extract.openapi.client.api.default_api.DefaultApi.status_task_id_get",
        return_value={
            'current': 100,
            'message': 'completed',
            'result': {},
            'state': 'SUCCESS',
            'total': 100.0
        }
    )
    def test_status_response(self, path_status_task_id_get):
        status_response = self.extract_client.status(self.task_id)
        self.assertEqual(self.response_with_task_id, status_response)

    def test_status_failed_without_task_id(self):
        with self.assertRaises(Exception) as context:
            self.extract_client.status(task_id=None)

        self.assertTrue("Not set task_id" in str(context.exception))
