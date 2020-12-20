from _csv import reader
from math import ceil
from os import path
import time
import click

from file_format_converter.file_readers.csv_file_reader import CSVReader
from file_format_converter.file_writer.json_writer import JsonFileWriter
from file_format_converter.file_writer.xml_writer import XmlFileWriter


@click.command()
@click.argument('file', type=click.Path(exists=True))
@click.option("-o", "--output", default="output", help="Output file name without any extension, default is 'output.<format-extension>'")
@click.option("-tf", "--target-format", "target_format", default="JSON", help="Supported formats: JSON - XML, default is JSON")
@click.option("-sf", "--source-format", "source_format", help="Supported formats: CSV, default is CSV")
def main(file, output, source_format: str, target_format: str):
    file_writer = None
    file_reader = None

    if target_format is not None:
        target_format = "json"
    target_format = target_format.lower()

    if source_format is not None:
        source_format = "json"
    source_format = source_format.lower()

    if target_format.__eq__("xml"):
        file_writer = XmlFileWriter({"output": output})
    else:
        file_writer = JsonFileWriter({"output": output})

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

        file_reader = CSVReader(file)

        header = file_reader.get_item_names()
        header_index = {}
        for i, name in enumerate(header):
            header_index[i] = name
        file_writer.set_header(header_index)

        for row in file_reader.get_items():
            file_writer.save_item(row)
            valid_item += 1
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
        print("Valid item count: %s percent: %s" % (valid_item, (valid_item / total_item * 100)))
        print("Invalid item count: %s percent: %s" % (invalid_item, (invalid_item / total_item * 100)))


if __name__ == "__main__":
    main()
