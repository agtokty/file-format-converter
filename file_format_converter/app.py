import time
import click

from file_format_converter.file_readers.csv_file_reader import CSVReader
from file_format_converter.file_writer.json_writer import JsonFileWriter
from file_format_converter.file_writer.xml_writer import XmlFileWriter
from file_format_converter.rule_helper import RuleHelper

SUPPORTED_SOURCE_FORMATS = ["csv"]
SUPPORTED_TARGET_FORMATS = ["json", "xml"]


@click.command()
@click.argument('file', type=click.Path(exists=True))
@click.option("-o", "--output", default="output", help="Output file name without any extension, default is 'output.<format-extension>'")
@click.option("-r", "--rules", "rules_file_path", help="Rule definitions file")
@click.option("-tf", "--target-format", "target_format", default="json", help="Target data format",
              type=click.Choice(SUPPORTED_TARGET_FORMATS, case_sensitive=False))
@click.option("-sf", "--source-format", "source_format", default="csv", help="Source data format",
              type=click.Choice(SUPPORTED_SOURCE_FORMATS, case_sensitive=False))
@click.option('--formatted/--no-formatted', default=True, help="Indicated that target file will be formatted or not")
def main(file, output, rules_file_path, source_format: str, target_format: str, formatted: bool):
    if target_format is None:
        target_format = "json"
    target_format = target_format.lower()

    if source_format is None:
        source_format = "json"
    source_format = source_format.lower()

    writer_options = {
        "output": output,
        "formatted": formatted
    }

    file_writer = None
    file_reader = None

    if target_format.__eq__("xml"):
        file_writer = XmlFileWriter(writer_options)
    else:
        file_writer = JsonFileWriter(writer_options)

    if source_format.__eq__("csv"):
        file_reader = CSVReader(file)
    else:
        file_reader = CSVReader(file)

    total_item = 0
    valid_item = 0
    invalid_item = 0
    duration = 0

    try:
        start_time = time.time()

        header = file_reader.get_item_names()
        header_names = []  # header name indexes [header1, header2, ..]
        header_indexes = {}  # header name indexes {header1 : 0, header2 : 1 ..}

        for i, name in enumerate(header):
            header_names.append(name)
            header_indexes[name] = i

        file_writer.set_header(header_names)
        rule_helper = RuleHelper(rules_file_path, header_indexes)

        for row in file_reader.get_items():
            row, is_valid = rule_helper.apply(row)
            if is_valid:
                file_writer.save_item(row)
                valid_item += 1
            else:
                invalid_item += 1

            total_item += 1

        duration = (time.time() - start_time)
    except Exception as e:
        print(e)
        print("error happened")

    file_writer.close()

    if total_item > 0:
        print("Conversion is completed in %s ms" % (duration))
        print("Output file location: %s" % file_writer.get_result_location())
        print_stats(total_item, valid_item, invalid_item)


def print_stats(total_item, valid_item, invalid_item):
    if total_item > 0:
        print("Total items: %s" % total_item)
        print("Valid item count: %s percent: %s" % (valid_item, round(valid_item / total_item * 100)))
        print("Invalid item count: %s percent: %s" % (invalid_item, round(invalid_item / total_item * 100)))


if __name__ == "__main__":
    main()
