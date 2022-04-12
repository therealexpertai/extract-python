import os

import expertai.extract.openapi.client as openapi_client
from expertai.extract.openapi.client.api import default_api
from expertai.extract.openapi.client.model.layout_request import LayoutRequest
import base64
from expertai.extract.authentication import Authentication


class ExtractClient:
    def __init__(self, authorization_host=None, host=None):
        self.__authentication = Authentication(authorization_host)
        self.__host = host

    def __document_with_file_path(self, file_path=None, file_name=None):
        with open(file_path, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
            return {"name": file_name, "data": encoded_string.decode('utf-8')}

    def __layout_document_async_post_request(self, configuration, document):
        with openapi_client.ApiClient(configuration) as api_client:
            api_instance = default_api.DefaultApi(api_client)
            layout_request = LayoutRequest(document)

            try:
                return api_instance.layout_document_async_post(layout_request=layout_request)
            except openapi_client.ApiException as e:
                if e.status == 403:
                    print("Your account does not have subscription for Extract")
                else:
                    print("Exception when calling DefaultApi->layout_document_async_post: %s\n" % e)
        raise Exception("Exception when call layout_document_async")

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

        with openapi_client.ApiClient(configuration) as api_client:
            api_instance = default_api.DefaultApi(api_client)

            try:
                status = api_instance.status_task_id_get(task_id=task_id)
                return status
            except openapi_client.ApiException as e:
                if e.status == 403:
                    print("Your account does not have subscription for Extract")
                else:
                    print("Exception when calling DefaultApi->layout_document_async_post: %s\n" % e)
        raise Exception("Exception when call layout_document_async")
