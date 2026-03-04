import click
import logging

from gtfs2map.renderer import JinjaRenderer
from gtfs2map.context import GeoJsonContext


@click.group()
def cli():
    pass

@cli.command()
@click.option('--data', '-d', default='/data/geojson/gtfs2map.geojson', help='Filename of the input GeoJSON file.')
@click.option('--template', '-t', default='/data/j2/input', help='Directory where the template files are located.')
@click.option('--output', '-o', default='/data/html/output', help='Output directory for the result application files.')
def render(data: str, template: str, output: str):
    template_directory: str = template
    output_directory: str = output
    
    logging.info(f"Loading context ...")
    context: GeoJsonContext = GeoJsonContext(data)

    logging.info(f"Rendering output HTML ...")
    renderer: JinjaRenderer = JinjaRenderer(
        template_directory,
        output_directory
    )
    
    renderer.render(context.create())
    

if __name__ == '__main__':
     # set logging default configuration
    logging.basicConfig(format="[%(levelname)s] %(asctime)s %(message)s", level=logging.INFO)
    
    cli()