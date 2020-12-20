# File Format Converter

This is a simple cli program that helps you to convert your **structured** data files to other data formats like JSON and XML

## Features

* Conversations 
    * [x] Csv to Json - Xml
    * [ ] Json to Csv - Xml
    * [ ] Xml to Csv - Json
* Formatted and unformetted output option
* Validate and only transform valid data using rule definitions

# Installation

TODO - upload package to pypi 

Using pip 
```
pip install file-format-converter
```

Using docker 
```
# build docker image
docker build -t ffc .

# run with paramters
  docker run --rm  \
  -v $PWD/data:/data \
  ffc --rules rules.json --output /data/output /data/hotels.csv
```

# Usage

* Default target format is JSON
* Default output name is **output**

To get help on parameters
```
ffc --help
```

This will generate output.json
```
ffc myfile.csv
```


This will generate myxmlfile.xml
```
ffc -tf XML -o myxmlfile myfile.csv
```


This will generate unformatted output.xml, default is formatted.
```
ffc -tf XML --no-formatted myfile.csv
```

Use pre-defined rules
```
ffc -r rules.json myfile.csv
```

### Define Rules

You can define validation rules for each column in data before transformation to new format.
So, only valid rows will be transformed to new format

```
{
  "<column-name>": {
    "<rule-key>": {
      "<rule-param>": "<rule-param>"
    },
    ... // other rules
  },
  ...// other column rules
}
```

For example, following rule has the rules;

* **hotel** column value should only have up to 100 characters.
* **stars** column value should be a number from 0 to 5 value.
* **url** column value should syntactically valid url.

```
{
  "hotel": {
    "str-length": {
      "max": 100
    }
  },
  "stars": {
    "number": {
      "min": 0,
      "max": 5
    }
  },
  "url": {
    "url": true
  }
}
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

 TODO - find classes using module loading, not using if else...
 
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

 TODO - find classes using module loading, not using if else...
 
 ### Adding New Rule Implementations
 
 You can implement your custom rules using [rule.py](file_format_converter/api/rule.py) class.

 After implementation add your file to [here in rule_helper.py](file_format_converter/rule_helper.py#L8)
 
Currently implemented rules

| key         | Class       | Description |
| ----------- | ----------- | ----------- |
| **str-length**  | [StringLengthRule](file_format_converter/rules/string_length_rule.py) | Filter string values by their length       |
| **numeric**     | [NumericRule](file_format_converter/rules/numeric_rule.py)            | Filder numeric values       |
| **url**         | [UrlRule](file_format_converter/rules/url_rule.py)                    | Filter valid url       |

 TODO - find rule classes using module loading instead of static dict
 TODO - Support simple rule query like SQL where statements.