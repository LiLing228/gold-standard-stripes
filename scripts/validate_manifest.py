#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
validate_manifest.py

Validate a stripes.manifest TSV or CSV against manifest.schema.json
"""

import json
import pandas as pd
import argparse
import sys
from jsonschema import validate, ValidationError

def load_schema(schema_path):
    """Load JSON Schema"""
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_manifest(manifest_path, schema):
    """Validate manifest file (TSV or CSV) against schema"""

    sep = "\t" if manifest_path.endswith(".tsv") else ","
    df = pd.read_csv(manifest_path, sep=sep, dtype=str).fillna("")

    # Define fields that need to be coerced to integers
    int_fields = ["Resolution Bp", "Patch Matrix Size"]

    valid = True
    for idx, row in df.iterrows():
        data = row.to_dict()

        # Attempt to convert specified fields to integer
        for field in int_fields:
            if field in data and data[field] != "":
                try:
                    data[field] = int(data[field])
                except ValueError:
                    # Keep original value if conversion fails, validation will catch it
                    pass

        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            valid = False
            # Print row number (1-based), field name, and error message
            print(f"Row {idx+1} invalid:")
            print(f"  Error: {e.message}")
            if e.path:
                print(f"  Field: {'.'.join(str(p) for p in e.path)}")
            print("-"*50)

    if valid:
        print("All rows are valid!")
    else:
        print("Some rows are invalid. See messages above.")
    return valid

def main():
    parser = argparse.ArgumentParser(description="Validate stripes.manifest TSV/CSV against schema")
    parser.add_argument("manifest", help="Path to stripes.manifest.tsv or .csv")
    parser.add_argument("--schema", default="../manifest/manifest.schema.json",
                        help="Path to manifest.schema.json (default: ../manifest/manifest.schema.json)")
    args = parser.parse_args()

    schema = load_schema(args.schema)
    valid = validate_manifest(args.manifest, schema)
    sys.exit(0 if valid else 1)

if __name__ == "__main__":
    main()
