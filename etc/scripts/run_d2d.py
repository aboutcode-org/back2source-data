import csv
import os
import requests
from purldb_toolkit.purlcli import d2d
import json


def create_csv_from_json(json_files, csv_file):
    with open(csv_file, mode='w') as file:
        writer = csv.writer(file)
        header = [
            "path","uuid", "created_date", "resource_count", "package_count", "dependency_count", "relation_count",
            "codebase_resources_ignored_directory", "codebase_resources_no_licenses", "codebase_resources_scanned", "codebase_resources_not_deployed", "codebase_resources_requires_review",
            "discovered_packages_total", "discovered_packages_with_missing_resources", "discovered_packages_with_modified_resources",
            "discovered_dependencies_total", "discovered_dependencies_is_runtime", "discovered_dependencies_is_optional", "discovered_dependencies_is_resolved",
            "codebase_relations_dwarf_compiled_paths", "codebase_relations_dwarf_included_paths",
            "codebase_resources_discrepancies_total",
            "from_filename", "from_download_url", "from_is_uploaded", "from_size", "from_is_file", "from_exists",
            "to_filename", "to_download_url", "to_is_uploaded", "to_size", "to_is_file", "to_exists"
        ]
        writer.writerow(header)
        for json_file in json_files:
            data = json.load(open(json_file))
            input_sources = data["input_sources"]
            input_sources_dict = {}
            for input_source in input_sources:
                tag = input_source["tag"]
                for key, value in input_source.items():
                    if key == "tag":
                        continue
                    new_key = f"{tag}_{key}"
                    input_sources_dict[new_key] = value
            row = [
                json_file,
                data["uuid"], data["created_date"], data["resource_count"], data["package_count"], data["dependency_count"], data["relation_count"],
                data["codebase_resources_summary"]["ignored-directory"], data["codebase_resources_summary"].get("no-licenses") or "", data["codebase_resources_summary"].get("scanned") or "", data["codebase_resources_summary"].get("not-deployed") or "", data["codebase_resources_summary"]["requires-review"],
                data["discovered_packages_summary"]["total"], data["discovered_packages_summary"]["with_missing_resources"], data["discovered_packages_summary"]["with_modified_resources"],
                data["discovered_dependencies_summary"]["total"], data["discovered_dependencies_summary"]["is_runtime"], data["discovered_dependencies_summary"]["is_optional"], data["discovered_dependencies_summary"]["is_resolved"],
                data["codebase_relations_summary"].get("dwarf_compiled_paths") or "", data["codebase_relations_summary"].get("dwarf_included_paths") or "",
                data["codebase_resources_discrepancies"]["total"],
                input_sources_dict.get("from_filename", ""), input_sources_dict.get("from_download_url", ""), input_sources_dict.get("from_is_uploaded", ""), input_sources_dict.get("from_size", ""), input_sources_dict.get("from_is_file", ""), input_sources_dict.get("from_exists", ""),
                input_sources_dict.get("to_filename", ""), input_sources_dict.get("to_download_url", ""), input_sources_dict.get("to_is_uploaded", ""), input_sources_dict.get("to_size", ""), input_sources_dict.get("to_is_file", ""), input_sources_dict.get("to_exists", "")
            ]
            writer.writerow(row)


def run_d2d():
    from_to_urls = []
    with open("pairs.csv", "r") as f:
        for line in f:
            from_to = line.strip().split(",")
            from_to_urls.append({"to": from_to[0], "from": from_to[1]})

    paths = []

    for from_to_url in from_to_urls:
        from_url = from_to_url["from"]
        to_url = from_to_url["to"]
        
        try:
            r = requests.head(from_url, timeout=30)
        except:
            continue
        from_size = r.headers.get('content-length')
        from_size = int(from_size) if from_size else None

        if from_size and from_size > 10000000:
            continue

        try:
            r = requests.head(from_url, timeout=30)
        except:
            continue
        to_size = r.headers.get('content-length')
        to_size = int(to_size) if to_size else None

        url_path = from_url.split('#')[0]
        folder_name = url_path.split('/')[-1]
        folder_name_parts = folder_name.split('.')
        if folder_name_parts[-1] == 'rpm':
            folder_name = '.'.join(folder_name_parts[:-1])
        directory_path = os.path.dirname(url_path.replace('https://', ''))
        directory_path = "data/" + directory_path + "/" + folder_name
        os.makedirs(directory_path, exist_ok=True)
        file_path = os.path.join(directory_path, 'd2d-summary.json')

        if to_size and to_size > 10000000:
            continue
        try:
            d2d(
            purls=[
                from_url, to_url
            ], 
            output=file_path, 
            purldb_api_url=None, 
            matchcode_api_url="http://127.0.0.1:8002/api/"
            )
            paths.append(file_path)
        except:
            continue

    create_csv_from_json(paths, "d2d-summary.csv")


run_d2d()
