# LayoutItem

Layout element

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Element ID | [optional] 
**page** | **int** | Element page | [optional] 
**children** | **[int]** | List of child elements | [optional] 
**type** | **str** | Element type (\&quot;page\&quot;, \&quot;title\&quot;, \&quot;text\&quot;, \&quot;header\&quot;, \&quot;footer\&quot;, \&quot;table\&quot;, \&quot;cell\&quot;) | [optional] 
**parent** | **int** | Parent element ID | [optional] 
**label** | **str** | Element label (experimental) | [optional] 
**content** | **str** | Boxed element text | [optional] 
**bbox** | **[int]** | Bounding box coordinates in pixels: upper left corner X, upper left corner Y, lower right corner X and lower right corner Y. Coordinates are referred to a 100 DPI (dots per inch) rendering of the page. The coordinates origin is at the top left corner of the rendered page.  | [optional] 
**row** | **int** | (For table cells) Cell row | [optional] 
**column** | **int** | (For table cells) Cell column | [optional] 
**is_h_ead** | **bool** | (For table cells) true if cell is a column heading, false otherwise | [optional] 
**span** | **[int], none_type** | (For table cells) Column and row span or null | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


