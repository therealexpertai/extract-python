# extract-python
Python client for expert.ai Extract. 

<a href="https://docs.expert.ai/extract/latest/" target="_blank">**Extract**</a> is expert.ai "document understanding" Cloud API.  
It extracts text from PDF documents in a smart way: it detects pages and, inside them, headings, body-level text, tables, headers and footers. It returns all the blocks of text of each page in the same order in which a human would read them, so helping creating a stream of text than gives better results when applying Natural Language Processing (NLP).  
Knowing where text occurs, e.g. inside a table's cell, helps improve the quality of information extraction tasks because they can have a more accurate scope.

## Installation

To install the client library with `pip`:

```bash
pip install expertai-extract
```

To install using `conda`:

```bash
conda install -c conda-forge expertai-extract
```

## Usage

### Subcription and credentials
Currently Extract is in Beta testing phase, so you have to <a href="mailto:extractbeta@expert.ai">contact expert.ai</a>, describe your use case and ask to participate in the test program.  
If they say "yes", they will tell you what to do (you'll have to subscribe the Extract Beta plan from inside the developer portal) and then you can use Extract for free during the test phase.

This Python client needs to know your expert.ai dveloper account credentials, so you'll have to set these two environment variables:

    EAI_USERNAME
    EAI_PASSWORD

### Create the client
To use this client in your code, import the `ExtractClient` class:
    
    from expertai.extract.extract_client import ExtractClient

Then create an instance of the client object:

    extractClient = ExtractClient()

You can then invoke the object methods to use expert.ai Extract API

### Methods

**layout_document_async()**

Use the `layout_document_async()` method to analyze a document.  
The method corresponds to the <a href="https://docs.expert.ai/extract/latest/reference/layout-document-async/" target="_blank">`layout-document-async`</a> API resource and it starts an asyncronous layout recognition task. It returns the ID of that task.

There are two possible syntaxes:

<pre><code>layout_document_async(file_path=<i>filePath</i>, file_name=<i>fileName</i>)</code></pre>

and:

<pre><code>layout_document_async(file=<i>base64</i>, file_name=<i>fileName</i>)</code></pre>

_`filePath`_ is the path of the PDF file (including the file name), _`fileName`_ is the file name. _`base64`_ is the Base64 encoding of the PDF file.

_`fileName`_ is only the name (not the path) of the PDF file. If you use the first syntax, you are free to set _`fileName`_ to a different value than the name of the file specified in _`filePath`_, since _`fileName`_ is more of a "document name", but if you don't have any special reason for doing so, use the same value.

> Be aware of Extract limits: the maximum size of the PDF file you can analyze is 10MB and the document must have at most 500 pages.

The method returns a dictionary containing an item with key `task_id` which value (a string) is the ID of the layout recognition task. 
For example:
    
    from expertai.extract.extract_client import ExtractClient

    extractClient = ExtractClient()

    layoutRecognitionTask = extractClient.layout_document_async(file_path="test/resources/test.pdf", file_name="test.pdf")
    taskId = layoutRecognitionTask["task_id"]

You then have to call the `status()` method to know about the progress of that task and also to get results when the task is complete.

**Status**

Use the `status()` method to know about the progress of a layout recognition task that was started with the `layout_document_async()` method and to get results when the task is complete. It corresponds to the <a href="https://docs.expert.ai/extract/latest/reference/status/" target="_blank">`status`</a> API resource.

The syntax is:

<pre><code>status(<i>taskId</i>)</code></pre>

where _`taskID`_ is the ID of the layout recognition task returned by the `layout_document_async()` method.

The method returns an object with these properties:

- `current` (int): percentage of completion of the task
- `message` (str): phase of the task, for example `"page conversion"`, `"classification"`
- `result` (dict): results (when the task is complete)
- `state` (str): task status, for example `"PROGRESS"`, `"SUCCESS"`

If `current` is 100, the task is finished and `result` contains the results.  
The structure of the `result` dictionary reflects that of the JSON object returned by the `status` resource of the API.  
Refer to the <a href="https://docs.expert.ai/extract/latest/reference/results/" target="_blank">API documentation</a> or use the <a href="https://developer.expert.ai/ui/resources/extract/specification#" target="_blank">Swagger UI</a> in the developer portal to learn about the result structure.

## Examples

**Basic usage**

This example shows the basic usage of the client to start a recognition task, wait until it's finished and then print results.

    import time
    from expertai.extract.extract_client import ExtractClient

    extractClient = ExtractClient()

    layoutRecognitionTask = extractClient.layout_document_async(file_path="test/resources/test.pdf", file_name="test.pdf")
    taskId = layoutRecognitionTask["task_id"]

    status = extractClient.status(taskId)

    while status.state != "SUCCESS" and status.state != "FAILURE":
        print("Status: " + status.state + " ( " + str(status.current) + "% )")
        time.sleep(5)
        status = extractClient.status(taskId)

    print(status)

**Printing titles**

This example extends the previous to show how to print all the documents headings.

    import time
    from expertai.extract.extract_client import ExtractClient

    extractClient = ExtractClient()

    layoutRecognitionTask = extractClient.layout_document_async(file_path="test/resources/test.pdf", file_name="test.pdf")
    taskId = layoutRecognitionTask["task_id"]

    status = extractClient.status(taskId)

    while status.state != "SUCCESS" and status.state != "FAILURE":
        print("Status: " + status.state + " ( " + str(status.current) + "% )")
        time.sleep(5)
        status = extractClient.status(taskId)
    
    for layoutItem in status.result["layout"]:
        if layoutItem["type"] == "title":
            print(layoutItem["content"])

**Decoding and printing words**

This example extends the first to show how to decode and print the items of the `words` list.  
Each item in that list contains all the words of a page, no matter the type of block in which they are, together with their bounding box. Use words instead of layout items when you simply need all the text of a page (or document) in the correct reading order.  
To make API output as compact as possible, words are returned compressed and Base64-encoded. Refer to <a href="https://docs.expert.ai/extract/latest/reference/results/#words" target="_blank">the documentation</a> to more about this representation.

    import time
    import base64
    import gzip
    from expertai.extract.extract_client import ExtractClient

    extractClient = ExtractClient()

    layoutRecognitionTask = extractClient.layout_document_async(file_path="test/resources/test.pdf", file_name="test.pdf")
    taskId = layoutRecognitionTask["task_id"]

    status = extractClient.status(taskId)

    while status.state != "SUCCESS" and status.state != "FAILURE":
        print("Status: " + status.state + " ( " + str(status.current) + "% )")
        time.sleep(5)
        status = extractClient.status(taskId)
    
    words = status.result["words"]
    
    for item in words:
        encoded = gzip.decompress(base64.standard_b64decode(item))
        index = 0
        while index < len(encoded):
            index_old = index
            index = index + encoded[index:].find(b'\x00')
            text = bytes(encoded[index_old:index]).decode('utf-8')
            index += 1  # skip byte 0
            index_elem = int.from_bytes(encoded[index:index + 4], 'little')
            index += 4
            bbox = [int.from_bytes(encoded[i:i + 4], 'little') for i in range(index,
                                                                              index + 16, 4)]
            index += 16
            
            print(text, end=" ")
    
            # skip 4 elements of the array with byte 0
            index = index + 4