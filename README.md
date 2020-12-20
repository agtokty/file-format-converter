# File Format Converter

This cli program help you to convert your structured file to other data formats like JSON and XML

## Features

* [x] Csv to Json - Xml
* [ ] Json to Csv - Xml
* [ ] Xml to Csv - Json

# Usage

* Default target format is JSON
* Default output name is **output**

This will generate output.json
```
ffc myfile.csv
```


This will generate myxmlfile.xml
```
ffc -tf XML -o myxmlfile myfile.csv
```


This will generate formatted output.xml
```
ffc -tf XML --formatted myfile.csv
```


# Development

You can extend capabilities of this app by adding new source reader and target format generators.

### Adding New Reader

Currently only supported source file reader is csv reader. To add new one you can implement [file_reader.py](file_format_converter/api/file_reader.py) class.
After implementation you can add it to [app.py](file_format_converter/app.py) to initialize reader instance.

```
if source_format.__eq__("csv"):
    file_reader = CSVReader(file)
elif file_format.__eq__("<YOUR-FORMAT-NAME>""):
    out = YourNewReader({"output": output})
else:
    file_reader = CSVReader(file)
```

### Adding New Format Writer

Outputters are target format file writers. Current
Currently only supported target file formats are Json and Xml. 
To add new writer you can implement [file_writer.py](file_format_converter/api/file_writer.py) class.
After implementation you can add it to [app.py](file_format_converter/app.py) to initialize writer instance.

```
if file_format.__eq__("xml"):
    out = XmlOutputter({"output": output})
elif file_format.__eq__("<YOUR-FORMAT-NAME>""):
    out = YourNewFormatWriter({"output": output})
else:
    out = JsonOutputter({"output": output})
```