import click
import logging

from feedmap.renderer import JinjaRenderer
from feedmap.context import GeoJsonContext


@click.group()
def cli():
    pass

@cli.command()
def render():
    template_directory: str = '/data/j2/input'
    output_directory: str = '/data/html/output'
    
    logging.info(f"Loading context ...")
    context: GeoJsonContext = GeoJsonContext('/data/geojson/feedmap.geojson')

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