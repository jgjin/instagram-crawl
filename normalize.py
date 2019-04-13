"""Noramlize .json data to .csv for plotting."""

import csv
import json
import os
import sys
from time import strptime


def process_json(
        json_file_name,
        field,
):
    """Extract relevant data from <json_file_name>."""
    with open(json_file_name) as json_file:
        json_contents = json.load(json_file)
        if field in json_contents:
            return [
                json_file_name[
                    (json_file_name.index("/") + 1):
                    json_file_name.index(".json")
                ],
                json_contents["timestamp"],
                json_contents[field],
            ]
    return None



def main(
):
    """Noramlize .json data to .csv for plotting."""
    field = sys.argv[1]

    data = []
    data_dir = "posts-data"
    for _, _, posts_json in os.walk(data_dir):
        for post_json in posts_json:
            row = process_json(
                os.path.join(
                    data_dir,
                    post_json,
                ),
                field,
            )
            if row:
                data.append(row)

    data.sort(
        key=lambda row: strptime(row[1], "%Y-%m-%dT%H:%M:%S.000Z")
    )
    with open(f"{field}.csv", "w") as output:
        wtr = csv.writer(output)
        wtr.writerow(["post_id", "timestamp", field])
        for row in data:
            wtr.writerow(row)


if __name__ == "__main__":
    main()
