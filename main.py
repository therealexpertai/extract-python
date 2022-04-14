import time
from expertai.extract.extract_client import ExtractClient

extractClient = ExtractClient()

lda = extractClient.layout_document_async(file_path="test/resources/test.pdf", file_name="test.pdf")
taskId = lda["task_id"]
print(taskId)
status = extractClient.status(taskId)
while status.state == "PENDING" or status.state == "PROGRESS":
    print("Status: " + status.state + " ( " + str(status.current) + "% )")
    time.sleep(2)
    status = extractClient.status(taskId)
print(status)
