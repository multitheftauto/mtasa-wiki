import logging
import os
import shutil
import jinja2
import http
import subprocess
import signal
from datetime import date
from pathlib import Path
import markdown

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
                            self.remove_function_repeated_defs(function)
                            
                            function['real_path'] = file_path
                            # Get name of parent folder
                            function["folder"] = os.path.basename(os.path.dirname(file_path))

                            for type_name in ['shared', 'client', 'server']:
                                type_info = function.get(type_name, {})
                                if not type_info:
                                    continue
                                if 'examples' in type_info:
                                    function["has_example"] = True
                                if 'issues' in type_info:
                                    function["has_issue"] = True

                            function_name = self.get_function_name(function)
                            function["name"] = function_name
                            function_type_name = self.get_function_type_name(function)
                            function["type_name"] = function_type_name

                            self.parse_function_examples(function)
                            self.parse_function_preview_images(function)

                            self.functions.append(function)
                    except Exception as e:
                        raise WikiBuilderError(f'Error loading function {file_path}: {e}')

    def get_function_type(self, function):
        return function.get('shared') or function.get('client') or function.get('server')
    
    def get_function_type_name(self, function):
        return function.get('shared') and 'shared' or function.get('client') and 'client' or function.get('server') and 'server'

    def get_function_name(self, function):
        return self.get_function_type(function).get('name')

    def remove_function_repeated_defs(self, function):
        # If a function is shared, remove client/server definitions that are the same as the shared one
        shared = function.get('shared')
        if not shared:
            return
        
        for type_name in ['client', 'server']:
            type_info = function.get(type_name)
            if not type_info:
                continue
            for key in shared.keys():
                if key in type_info and shared[key] == type_info[key]:
                    del type_info[key]

    def resolve_relative_or_repo_absolute_path(self, folder, path):
        if path.startswith('/'):
            return os.path.join(DOCS_REPO_PATH, path[1:])
        return os.path.join(folder, path)

    def parse_function_examples(self, function):
        examples = {}
        for type_name in ['shared', 'client', 'server']:
            type_info = function.get(type_name, {})
            if not type_info:
                continue
            examples[type_name] = []
            for example in type_info.get('examples', []):
                example_path = example.get('path')
                real_path = self.resolve_relative_or_repo_absolute_path(os.path.dirname(function.get('real_path')), example_path)
                if not os.path.exists(real_path):
                    raise WikiBuilderError(f'Example file not found: {real_path}')
                    return
                with open(real_path, 'r') as file:
                    example_code = file.read()
                
                examples[type_name].append({
                    'path': example_path,
                    'description': example.get('description'),
                    'code': example_code
                })
                type_info['examples'] = examples[type_name]

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
                
                # Ignore if destination file already exists
                if os.path.exists(output_path):
                    continue

                shutil.copyfile(real_path, output_path)
                self.logger.info(f"Created function preview image {output_path}")

                preview_images[type_name].append({
                    'real_path': real_path,
                    'path_html': f"/function_images/{base_name}",
                    'description': preview_img.get('description'),
                })
                type_info['preview_images'] = preview_images[type_name]

    def render_page(self, title, content):
        return self.layout_template.render(
            preview_mode = os.environ.get('CI_PREVIEW', True),
            year = date.today().year,
            title = title,
            navigation = self.navigation,
            content = content
        )
    
    def create_function(self, function_name):

        for function2 in self.functions:
            if function2['name'] == function_name:
                function = function2
                break
        if not function:
            raise WikiBuilderError(f'Function not found: {function_name}')
            return

        function_template = self.input_env.get_template('function.html')
        html_content = self.render_page(function['name'], function_template.render(function=function))

        web_path = f"/{function['name']}/"
        function_folder = OUTPUT_HTML_PATH + web_path

        Path(function_folder).mkdir(parents=True, exist_ok=True)

        output_path = os.path.join(function_folder, 'index.html')
        with open(output_path, 'w') as html_file:
            html_file.write(html_content)

        function["path_html"] = web_path

        self.logger.info(f"Generated {output_path}")

        return function

    def create_article(self, article_name, articles_folder='', custom_web_path=False):
        article_real_path = os.path.join(DOCS_REPO_PATH, 'articles', articles_folder, article_name, f"article.yaml")
        article = utils.load_and_validate_yaml(article_real_path, self.schema_article)
        
        content_path = article.get('content')
        content_real_path = self.resolve_relative_or_repo_absolute_path(os.path.dirname(article_real_path), content_path)
        with open(content_real_path, 'r') as content_file:
            article['content'] = content_file.read()
        
        article_template = self.input_env.get_template('article.html')
        article["html_content"] = markdown.markdown(article['content'])
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
                    function = self.create_function(function['name'])
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

    def create_misc_pages(self):

        # Predefined articles
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
                'name': 'Guides',
                'subitems': [
                    {
                        'name': 'Official guides',
                        'path_html': '/guides/official',
                        'category': {
                            'name': 'Official guides',
                            'articles': {
                                'path': 'official-guides',
                            },
                        },
                    },
                    {
                        'name': 'Community guides',
                        'path_html': '/guides/community',
                        'category': {
                            'name': 'Community guides',
                            'articles': {
                                'path': 'community-guides',
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

        self.create_misc_pages()
            
        
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
