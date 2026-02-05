#!/usr/bin/env python3
import json
import jsonschema
import sys
import argparse
from pathlib import Path

def validate_os_list(schema_path, json_path):
    """Validate an OS list JSON file against the schema."""
    try:
        # Load schema
        with open(schema_path) as f:
            schema = json.load(f)
        
        # Load OS list
        with open(json_path) as f:
            os_list = json.load(f)
        
        # Validate
        jsonschema.validate(instance=os_list, schema=schema)
        print(f"✓ {json_path} is valid against {schema_path}")
        return True
    except FileNotFoundError as e:
        print(f"✗ File not found: {e.filename}")
        return False
    except json.JSONDecodeError as e:
        print(f"✗ JSON decode error in {json_path if 'os_list' in locals() else schema_path}: {e.msg}")
        return False
    except jsonschema.exceptions.ValidationError as e:
        print(f"✗ Validation error in {json_path}:")
        print(f"  Path: {'.'.join(str(p) for p in e.path)}")
        print(f"  Error: {e.message}")
        return False
    except jsonschema.exceptions.SchemaError as e:
        print(f"✗ Schema error in {schema_path}: {e.message}")
        return False
    except Exception as e:
        print(f"✗ An unexpected error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate RPi Imager OS list JSON against schema.")
    parser.add_argument("json_path", help="Path to the JSON file to validate")
    parser.add_argument("--schema", default="doc/json-schema/os-list-schema.json", help="Path to the schema file")
    
    args = parser.parse_args()
    
    if not validate_os_list(args.schema, args.json_path):
        sys.exit(1)
