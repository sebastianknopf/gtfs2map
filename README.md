# gtfs2map
Utility for creating beautiful, usable maps visualizing GTFS-RT data. Based on:

- [gtfs-to-geojson](https://github.com/BlinkTagInc/gtfs-to-geojson) for generating geospatial data out of a GTFS feed
- [Jinja2](https://github.com/pallets/jinja) as templating engine

`gtfs2map` stands for `GTFS to Map` and provides an integrated stack for generating maps based on static GTFS data and then display GTFS-RT data inside this map. The main purporse is displaying vehicle positons, but also trip updates and service alerts are supported. During the rendering process, static HTML pages are generated which can be uploaded to each web server.

The `default` layout is highly configurable and provides an optimal entry point for starting with realtime maps. It uses no resource consuming JavaScript frameworks, but only basic CSS and JavaScript. If you want to provide your own theme, create a new folder below the `view` directory and set your theme in the configuration.

## Configuration & Running
There're some basic configurations affecting the behaviour of `gtfs2map`:

| Variable | Description |
| -- | -- |
| GTFS_STATIC_URL | URL to the static GTFS feed which should be used for rendering the static data. |
| GTFS_REALTIME_TRIP_UPDATES_URL | URL for the GTFS-RT trip updates consumed in the frontend. |
| GTFS_REALTIME_VEHICLE_POSITIONS_URL | URL to the GTFS-RT vehicle positions consumed in the frontend. |
| GTFS_REALTIME_SERVICE_ALERTS_URL | URL to the GTFS-RT service alerts consumed in the frontend. |

The variables starting with `APP_TEMPLATE_` are also available in the Jinja2 templates for rendering:
| Variable | Description |
| --- | --- |
| APP_TEMPLATE_ID | Name of the template for the resulting map. |
| APP_TEMPLATE_TITLE | Title for the single pages in the frontend. |
| APP_TEMPLATE_COLOR | Main theme color for the pages in the frontend. |
| APP_DATETIME_FORMAT | Format for displaying date and time values combined. Later used in moment.js in the frontend. |
| APP_DATE_FORMAT | Format for displaying date values. Later used in moment.js in the frontend. |
| APP_TIME_FORMAT | Format for displaying time values. Later used in moment.js in the frontend. |
| APP_UNMATCHED_VEHICLES_ENABLED | Boolean flag for allowing display of vehicles without assigned trip. |
| APP_TEMPLATE_CREDITS | Boolean flag for showing / hiding the credits in the footer. |

For rendering your map, using the pre-configured docker compose stack is strictly recommended. After selecting (or creating your own) layout by setting `APP_TEMPLATE_ID`, simply run:

```bash
docker compose run --rm gtfs2map render
```

## License
This project is licensed under the Apache License. See [LICENSE.md](LICENSE.md) for more information.