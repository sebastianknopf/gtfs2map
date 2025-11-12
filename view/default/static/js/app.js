function showMenu() {
	document.getElementById('app-menu').classList.remove('w3-hide-small');
	document.getElementById('app-menu').classList.remove('w3-hide-medium');
	
	document.getElementById('app-action-open-menu').classList.add('w3-hide');
	document.getElementById('app-action-close-menu').classList.remove('w3-hide');
}
 
function hideMenu() {
	document.getElementById('app-menu').classList.add('w3-hide-small');
	document.getElementById('app-menu').classList.add('w3-hide-medium');
	
	document.getElementById('app-action-open-menu').classList.remove('w3-hide');
	document.getElementById('app-action-close-menu').classList.add('w3-hide');
}

function onRouteItemClick(routeId) {
    window.location.href = `routes/${routeId}.html`;
}

function getGeoJsonBounds(geojson) {
    const bounds = new maplibregl.LngLatBounds();
	
    geojson.features.forEach(feature => {
        const geom = feature.geometry;
        if (geom.type === 'LineString') {
            geom.coordinates.forEach(coord => bounds.extend(coord));
        } else if (geom.type === 'MultiLineString') {
            geom.coordinates.forEach(line => line.forEach(coord => bounds.extend(coord)));
        }
    });

    return bounds;
}

async function fetchGtfsRealtimeData(url, headers) {
    if (!url) {
        return null;
    }

    const response = await fetch(url, {
        headers: { ...(headers ?? {}) },
    });

    if (!response.ok) {
        throw new Error(response.status);
    }

    const arrayBuffer = await response.arrayBuffer();
    const protocolBuffer = new Pbf(new Uint8Array(arrayBuffer));
    const obj = FeedMessage.read(protocolBuffer);

    return obj.entity;
}