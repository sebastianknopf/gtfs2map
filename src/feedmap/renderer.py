import colorsys
import geojson
import logging
import os
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
        
        os.makedirs(self._output_dir, exist_ok=True)

    def render_file(self, context: dict, filename: str) -> str:
        template: Template = self._env.get_template(filename)
        rendered: str = template.render(**context)

        return rendered
    
    def render(self, context: dict) -> None:
        """if os.path.exists(self._output_dir):
            shutil.rmtree(self._output_dir)
            os.makedirs(self._output_dir, exist_ok=True)"""
        
        for root, dirs, files in os.walk(self._template_directory):
            relative_path: str = os.path.relpath(root, self._template_directory)
            if relative_path == '.':
                relative_path = ''

            output_path: str = os.path.join(self._output_dir, relative_path)                
            os.makedirs(output_path, exist_ok=True)

            for filename in files:
                src_file: str = os.path.join(root, filename)

                if filename.endswith('.html.j2') or filename.endswith('.css.j2') or filename.endswith('.js.j2'):
                    rendered: str = self.render_file(context, os.path.join(relative_path, filename))

                    dest_file: str = os.path.join(
                        output_path, 
                        os.path.basename(filename[:-3]) if filename.endswith('.j2') else os.path.basename(filename)
                    )

                    with open(dest_file, 'w', encoding='utf-8') as f:
                        f.write(rendered)

                    logging.info(f"Rendered: {dest_file}")

                elif not filename.endswith('.j2'):
                    dest_file = os.path.join(output_path, filename)
                    shutil.copy2(src_file, dest_file)

                    logging.info(f"Copied:  {dest_file}")

    def _shade_filter(self, hex_color: str, level: int = 0) -> str:
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 8:
            r, g, b, a = [int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4, 6)]
        else:
            r, g, b = [int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
            a = 1.0

        h, l, s = colorsys.rgb_to_hls(r, g, b)
        
        if level > 0:
            l = min(1.0, l * (1 + level * 0.3))
            s = max(0.0, s * 1.0)
        elif level < 0:
            l = max(0.0, l * (1 + level * 0.1))
            s = max(0.0, s * 0.9)
        else:
            l = l

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
    