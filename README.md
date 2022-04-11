# extract-python
Python client for expert.ai Extract API. 

Extract is an expert.ai Document-Understanding Service designed to transform documents with unstructured information,
such as PDFs, images, Word documents into structured data.
You can use this Python Client to add those capabilities to Python applications.

[Useful link for Extract API](https://docs.expert.ai/extract/latest/)

Our Python client provides a class whose methods get document and analyze it.

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

### Set credentials
You need a developer account to use expert.ai Extract API.  
Go on the [developer portal](https://developer.expert.ai/ui) and sign up.
Expert.ai Extract API has a free trial, so you can use it for free for 60 days.  
Your developer account credentials must be specified as environment variables:

    EAI_USERNAME=YOUR_USERNAME
    EAI_PASSWORD=YOUR_PASSWORD

Replace `YOUR_USERNAME` with the email address you specified during registration on the developer portal and `YOUR_PASSWORD` with the account password.

### Create the client
To use this client in your code, import the `ExtractClient` class:
    
    from expertai.extract.extract_client import ExtractClient

Then create an instance of the client object:

    extractClient = ExtractClient()

You can then invoke the object methods to use expert.ai Extract API

### Methods

ExtractClient class methods provides expert.ai Extract API capabilities.

**Layout document asynchronous method**

Use `layout_document_async()` method to analyze document. The response contains task_id which can be used to see the state and result for this document.

    extractoClient.layout_document_async(file_path="your_pdf_file_path", file_name="pdf_file_name")

or

    extractClient.layout_document_async(file="your_file_encoded_in_base64", file_name="pdf_file_name")

The response body contains task_id:
    
    lda = extractClient.layout_document_async(file_path="test/resources/test.pdf", file_name="test.pdf")
    taskId = lda["task_id"]

The task_id must be used in subsequent calls.

**Status**

Use `status()` method to get current document status of analyzed document.

    extractClient.status(taskId)

The response contains:

`current` - the percentage completion of the task.

`message` - indicating the phase of the task.

`result` - the object that contains the results.

`state` - the status of the task.

The response can be with state:
- Progress:
    ```
  {
       "current": 50, # index page currently in process
       "message": "...", # detailed message about current state
       "state": "PROGRESS" # task status
  }
  ```
- Failure:
    ```
  {
       "current": 0, # fix value
       "message": "...", # error message
       "state": "FAILURE" # task status
  }
  ```
- Success:
    ```
  {
       "current": 100, # fix value
       "message": "completed", # fix message
       "result": { result_data_from_analyze },
       "state": "SUCCESS" # task status
  }
  ```

## Successful end-of-task response

With successful task, finished without errors, the result JSON object contains:

```
"header": {
	"conversionDateTime": "task end date and time",
	"customInfo": {
		"property 1 name": "property value",
		"property 2 name": "property value",
		...
		"property n name": "property value",
	},
	"documentName": "document name",
	"errorPages": number of pages that were not analyzed,
	"totPages": total number of pages,
	"version": "engine version",
	"metadata": [
		metadata object 1,
		metadata object 2,
		...
		metadata object n
	]
},
"layout": [
	layout object 1,
	layout object 2,
	...
	layout object n
],
"tableOfContent": [
    {
        "content": "...",
        "layoutId": number of layout id,
        "level": number of level,
        "score": number of score,
        "source": "source name"
    },
    ...
    {
        "content": "...",
        "layoutId": number of layout id,
        "level": number of level,
        "score": number of score,
        "source": "source name"
    },
],
"words": [
	"encoded page 1 words",
	"encoded page 2 words",
	...
	"encoded page n words"
]
```

**In header part**

The `header` object contains information about the whole document.

- conversionDateTime - `conversionDateTime` is the date and time the detection task ended.
- customInfo - The properties of the `customInfo` object correspond to the properties of the PDF document.
Most common properties are:

  - `Author`: author
  - `CreationDate`: creation date and time
  - `Creator`: creator
  - `ModDate`: last modification date and time
  - `Producer`: generator application
- documentName - `documentName` is the document name.
- errorPages - `errorPages` is the number of pages that could not be analyzed.
- totPages - `totPages` is the total number of pages.
- version - `version`  is the version of the software module that performed the detection task.
- metadata - `metadata` is an array of PDF metadata and it`s optional date that the PDF editor can insert into pages.

**In layout part**

`layout` is an array containing all the layout elements recognized in the document.  
Every item correspond to a layout element.  
The order of the elements in the array reflects the sequence of pages, so all the elements of page 1 are found first, then those of page 2, and so on.  
Within the elements of a page, the first element represents the page itself and the other elements are blocks of text or tables. The position of text blocks and tables in the array corresponds to what Extract assumed to be the order in which a human would read them on the page.  
Each item in the array is an object with these properties:

- `id`: block ID. Every block of text as a unique ID which can be referenced in the `children` or in the `parent` properties of other blocks.
- `page`: page number
- `children`: list of child blocks. This property is an array, each item of which is the ID of an element that is hierarchically a child of this element. For example, the titles in a page are children of the page element, the cells of a table are the children of a table element.
- `type`: element type, can be `page`, `title`, `text`, `header`, `footer`, `table` or `cell`.
- `parent`: parent element ID. In the case of table cells (`type` set to `cell`), the value of this property is the ID of the table element, while for title, text, header and footer blocks is the page element. Page elements don't have this property.
- `label`: element label. This is an experimental feature and must be ignored.
- `content`: block text, this property is absent in page and table elements.
- `bbox`: array containing the coordinates of the element's bounding box.

	- item 0: upper left corner X
	- item 1: upper left corner Y
	- item 2: lower right corner X
	- item 3: lower right corner Y
	
    Coordinates are in pixels and referred to a 100 DPI (dots per inch) rendering of the page. The coordinates origin is at the top left corner of the rendered page.

- `row`: cell row number, only for cell elements (`type` set to `cell`).
- `column`: cell column number, only for cell elements (`type` set to `cell`).
- `isHead`: set to `true` if the cell is a column header. Only for cell elements (`type` set to `cell`).
- `span`: cell span. It's an array of integer numbers. When present, the cell spans over more than one row and/or columns. The first item of the array is the row span, the second is the column span. Only for cell elements (`type` set to `cell`).

**In part words**

The `words` array contains one item per page and each item represents, in an encoded and compressed form, all the words present on the page.

The value of the single item is encoded in Base64.  
The decoded value is a byte array in gzip format.  
The expanded byte array value is another byte array in which each word corresponds to a variable-length sequence of bytes with this structure:

<pre><code><span class="bordered"><i>UTF-8 encoded text</i></span>0x00<span class="bordered"><i>Parent element ID</i></span><span class="bordered"><i>Bounding box coordinates</i></span></code></pre>

## Examples with Extract Client

**Layout document async method example**

    import time
    from expertai.extract.extract_client import ExtractClient
    
    extractClient = ExtractClient()
    
    lda = extractClient.layout_document_async(file_path="your_pdf_file_path", file_name="file name")
    taskId = lda["task_id"]

    status = extractClient.status(taskId)

    while status.state == "PENDING" or status.state == "PROGRESS":
        print("Status: " + status.state + " ( " + str(status.current) + "% )")
        time.sleep(2)
        status = extractClient.status(taskId)

    print(status)

**Titles concatenation example**

    import time
    from expertai.extract.extracto_client import ExtractClient
    
    extractClient = ExtractClient()
    
    layout_document = extractClient.layout_document_async(file_path="your_pdf_file_path",
                                                           file_name="file name")
    taskId = layout_document['task_id']
    status = extractClient.status(taskId)
    
    while status.state != "SUCCESS":
        time.sleep(2)
        status = extractClient.status(taskId)
    
    titles = ""
    
    for el in status.result['layout']:
        if el['type'] == 'title':
            titles = titles + el['content']
    
    print(titles)

**Words decoding example**

    import time
    import base64
    import gzip
    
    from expertai.extract.extract_client import ExtractClient
    
    extractClient = ExtractClient()
    
    layout_document = extractClient.layout_document_async(file_path="your_pdf_file_path", file_name="file name")
    taskId = layout_document['task_id']
    status = extractClient.status(taskId)
    
    while status.state != "SUCCESS":
        time.sleep(2)
        status = extractClient.status(taskId)
    
    words = status.result['words']
    res = []
    
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
            res.append({
                'text': text,
                'index': index_elem,
                'bbox': bbox,
            })
    
            # skip 4 elements of the array with byte 0
            index = index + 4
    
    print(res)