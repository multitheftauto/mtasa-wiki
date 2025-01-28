import yaml
from jsonschema import validate, ValidationError
import markdown
import re

def load_schema(schema_path):
    with open(schema_path, 'r') as file:
        schema = yaml.safe_load(file)
    return schema

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        return data

def load_and_validate_yaml(file_path, schema):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        validate(instance=data, schema=schema)
        return data

def to_html(markdown_text, single_paragraph=False):
    html = markdown.markdown(markdown_text)
    if single_paragraph:
        html = re.sub(r'<p>(.*?)</p>', r'\1', html)
    return html

def replace_special_variables(wiki_builder, text):
    specials = re.findall(r'\{\{.*?\}\}', text)
    specials = [s[2:-2] for s in specials]
    for special in specials:
        r_text = None

        # List of Element types
        if special == 'elements_list':
            r_text = "<ul>"
            for element in wiki_builder.elements:
                r_text += f"<li><a href='{element['path_html']}'>{element['name'].capitalize()}</a></li>"
            r_text += "</ul>"

        if r_text:
            text = text.replace("{{" + special + "}}", r_text)

    return text
