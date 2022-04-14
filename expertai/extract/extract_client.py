import os

import expertai.extract.openapi.client as openapi_client
from expertai.extract.openapi.client.api import default_api
from expertai.extract.openapi.client.model.layout_request import LayoutRequest
import base64
from expertai.extract.authentication import Authentication
import json


class ExtractClient:
    def __init__(self, authorization_host=None, host=None):
        self.__authentication = Authentication(authorization_host)
        self.__host = host

    def __document_with_file_path(self, file_path=None, file_name=None):
        with open(file_path, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
            return {"name": file_name, "data": encoded_string.decode('utf-8')}

    def __check_exception(self, exception):
        if exception.status == 403:
            body = json.loads(exception.body)
            message_failed = body["message"] + " - "
            embedded = body["_embedded"]
            errors = embedded["errors"]
            for message in errors:
                message_failed += message["message"] + "\n"
            raise Exception(message_failed) from None
        else:
            raise Exception(exception) from None

    def __layout_document_async_post_request(self, configuration, document):
        api_client = openapi_client.ApiClient(configuration)
        api_instance = default_api.DefaultApi(api_client)
        layout_request = LayoutRequest(document)

        try:
            return api_instance.layout_document_async_post(layout_request=layout_request)
        except openapi_client.ApiException as e:
            self.__check_exception(e)

    def layout_document_async(self, file=None, file_path=None, file_name=None):
        configuration = openapi_client.Configuration(
            host=self.__host,
            access_token=self.__authentication.get_access_token()
        )

        if file and file_path is None and file_name:
            document = {"name": file_name, "data": file}
        elif file_path and file is None and file_name:
            if os.path.isfile(file_path) is False:
                raise Exception("Not correct file_path")
            document = self.__document_with_file_path(file_path, file_name)
        else:
            raise Exception("Not correct configurations")

        return self.__layout_document_async_post_request(configuration, document)

    def status(self, task_id):
        if task_id is None or task_id == '':
            raise Exception("Not set task_id")

        configuration = openapi_client.Configuration(
            host=self.__host,
            access_token=self.__authentication.get_access_token()
        )

        api_client = openapi_client.ApiClient(configuration)
        api_instance = default_api.DefaultApi(api_client)

        try:
            status = api_instance.status_task_id_get(task_id=task_id)
            return status
        except openapi_client.ApiException as e:
            self.__check_exception(e)

