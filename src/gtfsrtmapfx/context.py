import geojson
import os

from geojson import Feature, FeatureCollection, MultiLineString


class GeoJsonContext:
    def __init__(self, geojson_filename: str) -> None:
        self.geojson: FeatureCollection = geojson.load(open(geojson_filename))

    def create(self) -> dict:
        context: dict = dict()

        # load geojson data
        agencies: dict = dict()
        routes: list = list()
        stops: list = list()

        for feature in self.geojson.features:
            if feature.geometry.type == 'MultiLineString' and 'route_id' in feature.properties:
                
                # add general route object
                routes.append(feature)

                # aggregate for each agency
                if feature.properties.get('agency_id', None) is not None:
                    if feature.properties['agency_id'] not in agencies:
                        agency: Feature = Feature()
                        agency.properties['agency_id'] = feature.properties['agency_id']
                        agency.properties['agency_name'] = feature.properties.get('agency_name')
                        agency.properties['routes'] = []

                        agency.geometry = MultiLineString(coordinates=[])

                        agencies[feature.properties['agency_id']] = agency

                    agencies[feature.properties['agency_id']].properties['routes'].append(feature.properties)
                    agencies[feature.properties['agency_id']].geometry.coordinates.extend(feature.geometry.coordinates)

                else:
                    if None not in agencies:
                        agency: Feature = Feature()
                        agency.properties['agency_id'] = feature.properties['agency_id']
                        agency.properties['agency_name'] = feature.properties.get('agency_name')
                        agency.properties['routes'] = []

                        agency.geometry = MultiLineString(coordinates=[])

                        agencies[None] = agency

                    agencies[None].properties['routes'].append(feature.properties)
                    agencies[None].geometry.coordinates.extend(feature.geometry.coordinates)

            if feature.geometry.type == 'Point' and 'stop_id' in feature.properties:
                
                # add general stop object
                stops.append(feature)

        context['agencies'] = FeatureCollection(features=list(agencies.values()))
        context['routes'] = FeatureCollection(features=routes)
        context['stops'] = FeatureCollection(features=stops)

        # add environment variables
        context['GTFS_REALTIME_TRIP_UPDATES_URL'] = os.getenv('GTFS_REALTIME_TRIP_UPDATES_URL', None)
        context['GTFS_REALTIME_VEHICLE_POSITIONS_URL'] = os.getenv('GTFS_REALTIME_VEHICLE_POSITIONS_URL', None)
        context['GTFS_REALTIME_SERVICE_ALERTS_URL'] = os.getenv('GTFS_REALTIME_SERVICE_ALERTS_URL', None)

        context['APP_TEMPLATE_ID'] = os.getenv('APP_TEMPLATE_ID', 'default')
        context['APP_TEMPLATE_TITLE'] = os.getenv('APP_TEMPLATE_TITLE', 'Map')
        context['APP_TEMPLATE_COLOR'] = os.getenv('APP_TEMPLATE_COLOR', '#4caf50')
        context['APP_DATETIME_FORMAT'] = os.getenv('APP_DATETIME_FORMAT', 'DD.MM.YYYY HH:mm')
        context['APP_DATE_FORMAT'] = os.getenv('APP_DATE_FORMAT', 'DD.MM.YYYY')
        context['APP_TIME_FORMAT'] = os.getenv('APP_TIME_FORMAT', 'HH:mm')
        context['APP_TEMPLATE_CREDITS'] = os.getenv('APP_TEMPLATE_CREDITS', 'true').lower() == 'true'

        return context