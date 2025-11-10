import geojson
import os

from geojson import FeatureCollection


class GeoJsonContext:
    def __init__(self, geojson_filename: str) -> None:
        self.geojson: FeatureCollection = geojson.load(open(geojson_filename))

    def create(self) -> dict:
        context: dict = dict()

        context['FM_TEMPLATE_ID'] = os.getenv('FM_TEMPLATE_ID', 'default')
        context['FM_TEMPLATE_TITLE'] = os.getenv('FM_TEMPLATE_TITLE', 'FeedMap')
        context['FM_TEMPLATE_COLOR'] = os.getenv('FM_TEMPLATE_COLOR', '#4caf50')
        context['FM_TEMPLATE_CREDITS'] = os.getenv('FM_TEMPLATE_CREDITS', 'true').lower() == 'true'

        return context