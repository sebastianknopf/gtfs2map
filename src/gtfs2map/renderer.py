import colorsys
import geojson
import json
import logging
import os
import requests
import shutil

from geojson import Feature
from jinja2 import Environment, Template, FileSystemLoader

class JinjaRenderer:

    def __init__(self, template_dir: str, output_dir: str) -> None:
        self._template_directory: str = template_dir
        self._output_dir: str = output_dir

        self._env: Environment = Environment(loader=FileSystemLoader(self._template_directory))
        self._env.filters['shade'] = self._shade_filter
        self._env.filters['text'] = self._text_filter
        self._env.filters['geojson'] = self._geojson_filter
        self._env.filters['properties'] = self._properties_filter
        self._env.filters['safe'] = self._safe_filter
        
        if os.path.exists(self._output_dir):
            for filename in os.listdir(self._output_dir):
                absolute_filename: str = os.path.join(self._output_dir, filename)
                try:
                    if os.path.isfile(absolute_filename) or os.path.islink(absolute_filename):
                        os.unlink(absolute_filename)
                    elif os.path.isdir(absolute_filename):
                        shutil.rmtree(absolute_filename)
                except Exception:
                    pass
        else:
            os.makedirs(self._output_dir, exist_ok=True)

        self._auto_render_extensions = ['.html.j2', '.css.j2', '.js.j2', '.geojson.j2']
        self._mandatory_render_filenames = ['index.html.j2', 'route.html.j2']

    def render_file(self, context: dict, filename: str) -> str:
        template: Template = self._env.get_template(filename)
        rendered: str = template.render(**context)

        return rendered
    
    def render(self, context: dict) -> None:
        
        ###
        # render mandatory files
        ###

        # index.html
        rendered: str = self.render_file(context, 'index.html.j2')

        index_output_file: str = os.path.join(self._output_dir, 'index.html')
        with open(index_output_file, 'w', encoding='utf-8') as f:
            f.write(rendered)

        logging.info(f"Rendered index.html [Mandatory]")

        # [route].html for each route
        for route in context.get('routes').features:
            rendered = self.render_file(
                {**context, 'route': route}, 
                'route.html.j2'
            )

            route_output_file: str = f"{self._safe_filter(route.properties['route_id'])}.html"
            with open(os.path.join(self._output_dir, route_output_file), 'w', encoding='utf-8') as f:
                f.write(rendered)

            logging.info(f"Rendered {route_output_file} [Mandatory]")
        
        ###
        # render everything else
        ### 
        for root, dirs, files in os.walk(self._template_directory):
            relative_path: str = os.path.relpath(root, self._template_directory)
            if relative_path == '.':
                relative_path = ''

            if relative_path == 'components':
                continue

            output_path: str = os.path.join(self._output_dir, relative_path)                
            os.makedirs(output_path, exist_ok=True)

            for filename in files:
                src_file: str = os.path.join(root, filename)

                if any([filename.endswith(ext) for ext in self._auto_render_extensions]):
                    relative_filename: str = os.path.join(relative_path, filename)
                    if relative_filename in self._mandatory_render_filenames:
                        continue
                    
                    rendered: str = self.render_file(context, relative_filename)

                    dest_file: str = os.path.join(
                        output_path, 
                        os.path.basename(filename[:-3]) if filename.endswith('.j2') else os.path.basename(filename)
                    )

                    with open(dest_file, 'w', encoding='utf-8') as f:
                        f.write(rendered)

                    logging.info(f"Rendered {relative_filename}")

                elif not filename.endswith('.j2'):
                    if filename == 'packages.json':
                        continue

                    dest_file: str = os.path.join(relative_path, filename)
                    shutil.copy2(src_file, os.path.join(self._output_dir, dest_file))

                    logging.info(f"Copied {dest_file}")

        ###
        # download packages
        ###

        if os.path.exists(os.path.join(self._template_directory, 'packages.json')):
            with open(os.path.join(self._template_directory, 'packages.json'), 'r', encoding='utf-8') as f:
                packages = json.load(f)

            for package, destination in packages.items():
                destination = os.path.join(self._output_dir, destination)

                unpgk_url: str = f"https://unpkg.com/{package}"
                try:
                    response = requests.get(unpgk_url)
                    response.raise_for_status()

                    destination_directory: str = os.path.dirname(destination)
                    os.makedirs(destination_directory, exist_ok=True)

                    with open(destination, 'wb') as f:
                        f.write(response.content)

                    logging.info(f"Downloaded {unpgk_url} to {destination}")
                except requests.RequestException as e:
                    logging.error(f"Failed to download {unpgk_url}: {e}")

    def _shade_filter(self, hex_color: str, level: int = 0) -> str:
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 8:
            r, g, b, a = [int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4, 6)]
        else:
            r, g, b = [int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
            a = 1.0
        
        if level > 0:
            h, l, s = colorsys.rgb_to_hls(r, g, b)

            l = min(1.0, l * (1 + level * 0.385))
            s = max(0.0, s * 1.0)

            r, g, b = colorsys.hls_to_rgb(h, l, s)
        elif level < 0:
            h, l, s = colorsys.rgb_to_hls(r, g, b)

            l = max(0.0, l * (1 + level * 0.1))
            s = max(0.0, s * 0.9)

            r, g, b = colorsys.hls_to_rgb(h, l, s)
        
        r, g, b = int(r*255), int(g*255), int(b*255)
        a = int(a*255)

        if a < 255:
            return f"#{r:02x}{g:02x}{b:02x}{a:02x}"
        else:
            return f"#{r:02x}{g:02x}{b:02x}"
    
    def _text_filter(self, hex_color: str, level: int = 0) -> str:
        hex_color = self._shade_filter(hex_color, level)
        hex_color = hex_color.lstrip('#')
        r, g, b = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

        brightness: float = (r * 299 + g * 587 + b * 114) / 1000

        return "#000000" if brightness > 140 else "#ffffff"
    
    def _geojson_filter(self, feature: Feature) -> str:
        return geojson.dumps(feature)
    
    def _properties_filter(self, feature: dict|Feature, propname: str = None) -> dict:
        if propname is not None:
            if isinstance(feature, Feature):
                return feature.properties.get(propname, None)
            else:
                return feature.get(propname, None)
        else:
            if isinstance(feature, Feature):
                return feature.properties
            else:
                return feature
            
    def _safe_filter(self, value: str) -> str:
        value = value.replace('\\', '_')
        value = value.replace('/', '_')
        value = value.replace('&', '_')
        value = value.replace('%', '_')
        value = value.replace(':', '_')
        value = value.replace('?', '_')
        value = value.replace('#', '_')
        value = value.replace('"', '_')

        return value