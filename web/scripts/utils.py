import yaml
from jsonschema import validate, ValidationError

def load_schema(schema_path):
    with open(schema_path, 'r') as file:
        schema = yaml.safe_load(file)
    return schema

def load_and_validate_yaml(file_path, schema):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        validate(instance=data, schema=schema)
        return data
