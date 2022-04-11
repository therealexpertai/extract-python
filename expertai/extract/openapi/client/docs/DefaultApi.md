# openapi_client.DefaultApi

All URIs are relative to *http://extract.expert.ai/beta*

Method | HTTP request | Description
------------- | ------------- | -------------
[**layout_document_async_post**](DefaultApi.md#layout_document_async_post) | **POST** /layout-document-async | 
[**status_task_id_get**](DefaultApi.md#status_task_id_get) | **GET** /status/{task-id} | 


# **layout_document_async_post**
> LayoutDocumentAsyncResponse layout_document_async_post()



Asynchronous layout recognition.   The response body is a JSON object containing the ID of the recognition task. The task ID must be used in the URL of the `status` resource. 

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import time
import expertai.extract.openapi.client
from expertai.extract.openapi.client.api import default_api
from expertai.extract.openapi.client.model.layout_request import LayoutRequest
from expertai.extract.openapi.client.model.layout_document_async_response import LayoutDocumentAsyncResponse
from pprint import pprint
# Defining the host is optional and defaults to http://extract.expert.ai/beta
# See configuration.py for a list of all supported configuration parameters.
configuration = expertai.extract.openapi.client.Configuration(
    host = "http://extract.expert.ai/beta"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): bearerAuth
configuration = expertai.extract.openapi.client.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with expertai.extract.openapi.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    layout_request = LayoutRequest(None) # LayoutRequest | The document to be analyzed (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.layout_document_async_post(layout_request=layout_request)
        pprint(api_response)
    except expertai.extract.openapi.client.ApiException as e:
        print("Exception when calling DefaultApi->layout_document_async_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **layout_request** | [**LayoutRequest**](LayoutRequest.md)| The document to be analyzed | [optional]

### Return type

[**LayoutDocumentAsyncResponse**](LayoutDocumentAsyncResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Accepted |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**405** | Method Not Allowed |  -  |
**413** | Request Entity Too Large |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **status_task_id_get**
> RecognitionTaskOutput status_task_id_get(task_id)



Returns the status of the layout recognition task or, if the task is finished, the results of the task.   The task ID is that returned by the `layout-document-async` resource. 

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import time
import expertai.extract.openapi.client
from expertai.extract.openapi.client.api import default_api
from expertai.estratto.openapi.client.model.recognition_task_output import RecognitionTaskOutput
from pprint import pprint
# Defining the host is optional and defaults to http://extract.expert.ai/beta
# See configuration.py for a list of all supported configuration parameters.
configuration = expertai.estratto.openapi.client.Configuration(
    host = "http://extract.expert.ai/beta"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): bearerAuth
configuration = expertai.estratto.openapi.client.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with expertai.estratto.openapi.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    task_id = "task-id_example" # str | Recognition task ID

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.status_task_id_get(task_id)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->status_task_id_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_id** | **str**| Recognition task ID |

### Return type

[**RecognitionTaskOutput**](RecognitionTaskOutput.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**405** | Method Not Allowed |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

