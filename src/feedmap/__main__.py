import click
import logging


@click.group()
def cli():
    pass

@cli.command()
def render():
    logging.info("Rendering the feed map ...")


if __name__ == '__main__':
     # set logging default configuration
    logging.basicConfig(format="[%(levelname)s] %(asctime)s %(message)s", level=logging.INFO)
    
    cli()