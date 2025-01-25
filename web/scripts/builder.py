import logging
import os
import shutil
import jinja2
import http
import subprocess
import signal
from datetime import date
from pathlib import Path

import scripts.utils as utils

DOCS_REPO_PATH = os.getcwd() # Repository root
INPUT_RESOURCES_PATH = os.path.join(DOCS_REPO_PATH, "web/resources")
OUTPUT_HTML_PATH = os.path.join(DOCS_REPO_PATH, "web/output/html")

class WikiBuilderError(Exception):
    def __init__(self, message):
        super().__init__(message)

class WikiBuilder:
    
    def __init__(self, logger):
        self.logger = logger
        self.logger.info('Initializing WikiBuilder')

        parent_folder = os.path.basename(os.path.dirname(DOCS_REPO_PATH))
        if parent_folder == 'web' or parent_folder == 'tools':
            raise WikiBuilderError('ABORTING! Script must be executed from the root directory of the repository!')

    def build(self):
        self.clear()

        self.logger.info('Building wiki...')

        self.generate_wiki()

        self.logger.info('Done building wiki')

    def clear(self):
        self.logger.info('Clearing wiki build output...')

        if os.path.exists(OUTPUT_HTML_PATH):
            shutil.rmtree(OUTPUT_HTML_PATH)
            self.logger.info('Deleted %s', OUTPUT_HTML_PATH)
        else:
            self.logger.info('%s does not exist', OUTPUT_HTML_PATH)

        self.logger.info('Done clearing wiki build output')

    def load_schemas(self):
        try:
            self.schema_function = utils.load_schema(os.path.join(DOCS_REPO_PATH, 'schemas/function.yaml'))
            self.schema_article = utils.load_schema(os.path.join(DOCS_REPO_PATH, 'schemas/article.yaml'))
        except Exception as e:
            raise WikiBuilderError(f'Error loading schemas: {e}')

    def parse_functions(self):
        doc_folder = os.path.join(DOCS_REPO_PATH, 'functions')
        self.functions = []

        for root, _, files in os.walk(doc_folder):
            for filename in files:
                if filename.endswith('.yaml'):
                    file_path = os.path.join(root, filename)
                    try:
                        function = utils.load_and_validate_yaml(file_path, self.schema_function)
                        if function:
                            function = self.remove_function_repeated_defs(function)
                            
                            function['real_path'] = file_path
                            # Get name of parent folder
                            function["folder"] = os.path.basename(os.path.dirname(file_path))
                            
                            function_name = self.get_function_name(function)
                            function["name"] = function_name
                            function_type_name = self.get_function_type_name(function)
                            function["type_name"] = function_type_name

                            function = self.parse_function_examples(function)

                            function = self.parse_function_preview_images(function)

                            for type_name in ['shared', 'client', 'server']:
                                type_info = function.get(type_name, {})
                                if not type_info:
                                    continue
                                
                                # Is disabled? May be string message
                                function["disabled"] = type_info.get('disabled', False)

                                # Parse markdown to HTML in function
                                    
                                if 'description' in type_info:
                                    type_info['description_html'] = utils.to_html(type_info['description'])

                                if 'examples' in type_info:
                                    for example in type_info['examples']:
                                        if 'description' in example:
                                            example['description_html'] = utils.to_html(example['description'])

                                if 'issues' in type_info:
                                    for issue in type_info['issues']:
                                        issue['description_html'] = utils.to_html(issue['description'], single_paragraph=True)

                                if 'notes' in type_info:
                                    for note in type_info['notes']:
                                        note = utils.to_html(note, single_paragraph=True)

                                if 'preview_images' in type_info:
                                    for preview_img in type_info['preview_images']:
                                        if 'description' in preview_img:
                                            preview_img['description_html'] = utils.to_html(preview_img['description'], single_paragraph=True)

                            # Prepare parameters & returns for syntax display
                            syntaxes = {
                                'single': None,
                                'server': None,
                                'client': None,
                            }

                            parameters = []
                            returns = None
                            has_single_syntax = True
                            ignore_parameters = {
                                'client': None,
                                'server': None,
                            }

                            if function.get('shared'):
                                # Function may have different syntax for client/server
                                last_syntax_type = None
                                for type_name in ['shared', 'client', 'server']:
                                    type_info = function.get(type_name)
                                    if type_info and (type_info.get('parameters') or type_info.get('returns')):
                                        if last_syntax_type and last_syntax_type != type_name:
                                            has_single_syntax = False
                                            break
                                        last_syntax_type = type_name
                                # Check if client or server defs have ignore_parameters
                                for type_name in ['client', 'server']:
                                    type_info = function.get(type_name)
                                    if type_info:
                                        if type_info.get('ignore_parameters'):
                                            ignore_parameters[type_name] = type_info['ignore_parameters']
                                            has_single_syntax = False
                            else:
                                has_single_syntax = True

                            def parse_parameters_and_returns(parameters, returns):
                                syntax = {
                                    'arguments': {
                                        'required': [],
                                        'optional': []
                                    },
                                    'returns': {
                                        'values_type': None,
                                        'description': None,
                                        'values': []
                                    }
                                }
                                for parameter in parameters:
                                    parameter_custom = {
                                        'name': parameter.get('name'),
                                        'type': parameter.get('type'),
                                        'description_html': utils.to_html(parameter.get('description'), single_paragraph=True),
                                        'default': parameter.get('default'),
                                    }
                                    if parameter.get('default'):
                                        syntax['arguments']['optional'].append(parameter_custom)
                                    else:
                                        syntax['arguments']['required'].append(parameter_custom)
                                if returns:
                                    syntax['returns']['description_html'] = utils.to_html(returns.get('description'), single_paragraph=True)
                                    for value in returns.get('values'):
                                        syntax['returns']['values'].append(value)
                                    syntax['returns']['values_type'] = syntax['returns']['values'][0].get('type')

                                return syntax
                            
                            if has_single_syntax:
                                # Function has one single syntax defined in shared/client/server
                                type_info = function.get('shared') or function.get('client') or function.get('server')
                                parameters = type_info.get('parameters', [])
                                returns = type_info.get('returns', None)
                            
                                syntaxes['single'] = parse_parameters_and_returns(parameters, returns)
                            else:
                                # Get shared parameters and returns
                                shared = function.get('shared')
                                shared_parameters = shared.get('parameters', [])
                                shared_returns = shared.get('returns', None)

                                # Get client parameters and returns, complete missing with shared
                                client = function.get('client')
                                client_parameters = client.get('parameters') or shared_parameters
                                # Exclude ignore_parameters['client'] from client parameters
                                if ignore_parameters['client']:
                                    client_parameters = [p for p in client_parameters if p['name'] not in ignore_parameters['client']]
                                client_returns = client.get('returns') or shared_returns

                                # Get server parameters and returns, complete missing with shared
                                server = function.get('server')
                                server_parameters = server.get('parameters') or shared_parameters
                                # Exclude ignore_parameters['server'] from server parameters
                                if ignore_parameters['server']:
                                    server_parameters = [p for p in server_parameters if p['name'] not in ignore_parameters['server']]
                                server_returns = server.get('returns') or shared_returns

                                syntaxes['client'] = parse_parameters_and_returns(client_parameters, client_returns)
                                syntaxes['server'] = parse_parameters_and_returns(server_parameters, server_returns)

                            function['syntaxes'] = syntaxes

                            function['path_html'] = f"/{function['name']}/"

                            self.functions.append(function)
                    except Exception as e:
                        self.logger.exception(e)
                        raise WikiBuilderError(f'Error loading function {file_path}')

    def get_function_type(self, function):
        return function.get('shared') or function.get('client') or function.get('server')
    
    def get_function_type_name(self, function):
        return function.get('shared') and 'shared' or function.get('client') and 'client' or function.get('server') and 'server'

    def get_function_name(self, function):
        return self.get_function_type(function).get('name')

    def remove_function_repeated_defs(self, function):
        # If a function is shared, remove client/server definitions that are the same as the shared one
        shared = function.get('shared')
        if shared:
            for type_name in ['client', 'server']:
                type_info = function.get(type_name)
                if not type_info:
                    continue
                for key in shared.keys():
                    if key in type_info and shared[key] == type_info[key]:
                        del type_info[key]

        return function

    def resolve_relative_or_repo_absolute_path(self, folder, path):
        if path.startswith('/'):
            return os.path.join(DOCS_REPO_PATH, path[1:])
        return os.path.join(folder, path)

    def parse_function_examples(self, function):
        examples = {}
        example_number = 1
        for type_name in ['shared', 'client', 'server']:
            type_info = function.get(type_name, {})
            if not type_info:
                continue
            type_examples = type_info.get('examples')
            if not type_examples:
                continue
            function["has_example"] = True
            examples = []
            for example in type_examples:
                example_path = example.get('path')
                real_path = self.resolve_relative_or_repo_absolute_path(os.path.dirname(function.get('real_path')), example_path)
                if not os.path.exists(real_path):
                    raise WikiBuilderError(f'Example file not found: {real_path}')
                    return
                with open(real_path, 'r') as file:
                    example_code = file.read()
                
                examples.append({
                    'number': example_number,
                    'path': example_path,
                    'description': example.get('description', ''),
                    'code': example_code
                })
                example_number += 1
                type_info['examples'] = examples
        
        return function

    def parse_function_preview_images(self, function):
        preview_images = {}

        preview_images_folder = os.path.join(OUTPUT_HTML_PATH, 'function_images')
        os.makedirs(preview_images_folder, exist_ok=True)

        for type_name in ['shared', 'client', 'server']:
            type_info = function.get(type_name, {})
            if not type_info:
                continue
            preview_images[type_name] = []
            for preview_img in type_info.get('preview_images', []):
                real_path = self.resolve_relative_or_repo_absolute_path(os.path.dirname(function.get('real_path')), preview_img.get('path'))
                if not os.path.exists(real_path):
                    raise WikiBuilderError(f'Preview image not found: {real_path}')
                    return
                # Copy preview image
                base_name = os.path.basename(real_path)
                output_path = os.path.join(preview_images_folder, base_name)
                
                # Copy only if not already copied
                if not os.path.exists(output_path):
                    shutil.copyfile(real_path, output_path)
                    self.logger.info(f"Created function preview image {output_path}")

                preview_images[type_name].append({
                    'real_path': real_path,
                    'path_html': f"/function_images/{base_name}",
                    'description': preview_img.get('description', ''),
                })
                type_info['preview_images'] = preview_images[type_name]

        return function

    def render_page(self, title, content):
        return self.layout_template.render(
            wiki_version = self.wiki_version,
            preview_mode = os.environ.get('CI_PREVIEW', True),
            year = date.today().year,
            title = title,
            navigation = self.navigation,
            content = content
        )
    
    def create_function_page(self, function):
        function_template = self.input_env.get_template('function.html')
        html_content = self.render_page(function['name'], function_template.render(function=function))

        web_path = function["path_html"]
        function_folder = OUTPUT_HTML_PATH + web_path

        Path(function_folder).mkdir(parents=True, exist_ok=True)

        output_path = os.path.join(function_folder, 'index.html')
        with open(output_path, 'w') as html_file:
            html_file.write(html_content)

        self.logger.info(f"Generated {output_path}")

    def create_article(self, article_name, articles_folder='', custom_web_path=False):
        article_real_path = os.path.join(DOCS_REPO_PATH, 'articles', articles_folder, article_name, f"article.yaml")
        article = utils.load_and_validate_yaml(article_real_path, self.schema_article)
        
        content_path = article.get('content')
        content_real_path = self.resolve_relative_or_repo_absolute_path(os.path.dirname(article_real_path), content_path)
        with open(content_real_path, 'r') as content_file:
            article['content'] = content_file.read()
        
        article_template = self.input_env.get_template('article.html')
        article["content_html"] = utils.to_html(article['content'])
        html_content = self.render_page(
            article['title'],
            article_template.render(article=article)
        )
        if custom_web_path:
            web_path = custom_web_path
        else:
            web_path = f"/{article_name}/"
        article_folder = OUTPUT_HTML_PATH + web_path

        Path(article_folder).mkdir(parents=True, exist_ok=True)

        output_path = os.path.join(article_folder, 'index.html')
        with open(output_path, 'w') as html_file:
            html_file.write(html_content)

        article["path_html"] = web_path
        
        self.logger.info(f"Generated {output_path} for article {article_name}")

        return article

    def create_category(self, web_path, category_data):
        if category_data.get('subcategories'):
            for subcategory in category_data['subcategories']:
                this_web_path = web_path
                if 'articles' in subcategory:
                    articles = subcategory['articles']
                    this_web_path = f"{web_path}/{articles['path']}"
                elif 'functions' in subcategory:
                    functions = subcategory['functions']
                    fpath = functions['path']
                    ftype = functions['type']
                    this_web_path = f"/lua/functions/{ftype}/{fpath}"
                
                self.create_category(this_web_path, subcategory)

        category_name = category_data['name']
        items = []

        if web_path == '/':
            category_folder = OUTPUT_HTML_PATH
        else:
            category_folder = OUTPUT_HTML_PATH + web_path

        if 'articles' in category_data:
            articles_folder = category_data['articles']['path']
            # List folders in articles folder
            articles_folder_path = os.path.join(DOCS_REPO_PATH, 'articles', articles_folder)
            for article_name in os.listdir(articles_folder_path):
                if not os.path.isdir(os.path.join(articles_folder_path, article_name)):
                    continue
                article = self.create_article(article_name, articles_folder)
                items.append({
                    'name': article['title'],
                    'path_html': article['path_html']
                })
        elif 'functions' in category_data:
            functions_folder = category_data['functions']['path']
            functions_type = category_data['functions']['type']
            functions_folder_path = os.path.join(DOCS_REPO_PATH, 'functions', functions_folder)
            for function in self.functions:
                if function['type_name'] == functions_type and function['folder'] == functions_folder:
                    function["category"] = category_name
                    items.append({
                        'name': function['name'],
                        'path_html': function['path_html']
                    })
        elif 'subcategories' in category_data:
            # List subcategories
            for subcategory in category_data['subcategories']:
                subcat_name = subcategory['name']
                if 'functions' in subcategory:
                    functions_folder = subcategory['functions']['path']
                    functions_type = subcategory['functions']['type']
                    items.append({
                        'name': subcat_name,
                        'path_html': f"/lua/functions/{functions_type}/{functions_folder}"
                    })

        self.categories[category_name] = items

        category_template = self.input_env.get_template('category.html')
        html_content = self.render_page(category_name, category_template.render(
            category_name = category_name,
            items = items
        ))

        Path(category_folder).mkdir(parents=True, exist_ok=True)

        output_path = os.path.join(category_folder, 'index.html')
        with open(output_path, 'w') as html_file:
            html_file.write(html_content)
        
        self.logger.info(f"Generated {output_path} for category {category_name}")

    def create_pages(self):
        self.navigation = [
            {
                'name': 'Introduction',
                'path_html': '/',
                'article': {
                    'name': 'introduction',
                    'folder': '',
                },
            },
            {
                'name': 'Articles',
                'subitems': [
                    {
                        'name': 'Official articles',
                        'path_html': '/official',
                        'category': {
                            'name': 'Official articles',
                            'articles': {
                                'path': 'official',
                            },
                        },
                    },
                    {
                        'name': 'Community articles',
                        'path_html': '/community',
                        'category': {
                            'name': 'Community articles',
                            'articles': {
                                'path': 'community',
                            },
                        },
                    },
                ],
            },
            {
                'name': 'Functions',
                'subitems': [
                    {
                        'name': 'Client functions',
                        'path_html': '/lua/functions/client',
                        'category': {
                            'name': 'Client functions',
                            'subcategories': [
                                {
                                    'name': 'Client cursor functions',
                                    'functions': {
                                        'path': 'Cursor',
                                        'type': 'client',
                                    },
                                },
                            ],
                        },
                    },
                    {
                        'name': 'Shared functions',
                        'path_html': '/lua/functions/shared',
                        'category': {
                            'name': 'Shared functions',
                            'subcategories': [
                                {
                                    'name': 'Shared cursor functions',
                                    'functions': {
                                        'path': 'Cursor',
                                        'type': 'shared',
                                    },
                                },
                                {
                                    'name': 'Shared element functions',
                                    'functions': {
                                        'path': 'Element',
                                        'type': 'shared',
                                    },
                                },
                            ],
                        },
                    }
                ]
            }
        ]

        with open(os.path.join(DOCS_REPO_PATH, 'VERSION'), 'r') as file:
            self.wiki_version = file.read().strip()

        self.categories = {}

        def create_item(item):
            if 'article' in item:
                self.create_article(item['article']['name'], item['article']['folder'], item['path_html'])
            elif 'category' in item:
                self.create_category(item['path_html'], item['category'])
        
        for item in self.navigation:
            if 'subitems' in item:
                for subitem in item['subitems']:
                    create_item(subitem)
            else:
                create_item(item)
            
        # Generate related pages for each function
        for function in self.functions:
            function['related'] = []

            # Fill with the function's category items
            function_category = function.get('category')
            if function_category:
                category_items = self.categories.get(function_category)
                function['related'].append({
                    'category': function_category,
                    'items': category_items
                })

            # Fill with other see_also entries
            for type_name in ['shared', 'client', 'server']:
                type_info = function.get(type_name, {})
                if not type_info:
                    continue
                for see_also in type_info.get('see_also', []):
                    parts = see_also.split(':')
                    if len(parts) != 2:
                        continue
                    entry_type = parts[0]
                    entry_name = parts[1]
                    if entry_type == 'category':
                        category_items = self.categories.get(entry_name)
                        if category_items:
                            function['related'].append({
                                'category': entry_name,
                                'items': category_items
                            })

        # Create function pages
        for function in self.functions:
            self.create_function_page(function)

        # Other articles
        self.create_article('privacy')

        other_pages = [
            {
                'path_html': '404.html',
                'template': '404.html',
            },
        ]
        for page in other_pages:
            template = self.input_env.get_template(page['template'])
            html_content = self.render_page(page['path_html'], template.render())

            output_path = os.path.join(OUTPUT_HTML_PATH, page['path_html'])
            with open(output_path, 'w') as html_file:
                html_file.write(html_content)

            self.logger.info(f"Generated {output_path} for {page['path_html']}")

    def copy_assets(self):

        copy_files = [
            'favicon.ico', '_redirects',
        ]
        copy_folders = [
            'assets'
        ]

        for file in copy_files:
            shutil.copyfile(os.path.join(INPUT_RESOURCES_PATH, file), os.path.join(OUTPUT_HTML_PATH, file))
            self.logger.info(f"Copied file {file}")  

        for folder in copy_folders:
            shutil.copytree(os.path.join(INPUT_RESOURCES_PATH, folder), os.path.join(OUTPUT_HTML_PATH, folder))
            self.logger.info(f"Copied folder {folder}")
    
    def generate_wiki(self):
        self.load_schemas()
        self.parse_functions()

        self.input_env = jinja2.Environment(loader=jinja2.FileSystemLoader(INPUT_RESOURCES_PATH))
        
        self.layout_template = self.input_env.get_template('layout.html')

        self.create_pages()

        self.copy_assets()
