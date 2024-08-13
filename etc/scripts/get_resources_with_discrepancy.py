#
# Copyright (c) nexB Inc. and others. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/aboutcode-org/scancode.io for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import json
import os

# read all d2d-details.json files
# get all resources that has status "requires-review"

# get all files in data directory
data_dir = "data"
# json files are stored nested in directories
json_files = []
for root, dirs, files in os.walk(data_dir):
    for file in files:
        if file == "d2d-details.json":
            json_files.append(os.path.join(root, file))


# get all resources that has status "requires-review"
for json_file in json_files:
    resources_with_discrepancy = []
    print(json_file)
    summary_file = json_file.replace("d2d-details.json", "d2d-summary.json")
    summary_data = json.load(open(summary_file))
    data = json.load(open(json_file))
    for file in data["files"]:
        if file["status"] == "requires-review":
            extra_data = file.get("extra_data", {})
            dwarf_compiled_paths_not_mapped = extra_data.get("dwarf_compiled_paths_not_mapped", [])
            dwarf_included_paths_not_mapped = extra_data.get("dwarf_included_paths_not_mapped", [])
            resources_with_discrepancy.append(
                {
                    "path": file["path"],
                    "dwarf_compiled_paths_not_mapped_count": len(dwarf_compiled_paths_not_mapped),
                    "dwarf_included_paths_not_mapped_count": len(dwarf_included_paths_not_mapped),
                }
            )
    summary_data["resources_with_discrepancy"] = resources_with_discrepancy
    # write to json file
    with open(summary_file, "w") as f:
        json.dump(summary_data, f, indent=4)
