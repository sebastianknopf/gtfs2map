function showMenu() {
	document.getElementById('fm-app-menu').classList.remove('w3-hide-small');
	document.getElementById('fm-app-menu').classList.remove('w3-hide-medium');
	
	document.getElementById('fm-action-open-menu').classList.add('w3-hide');
	document.getElementById('fm-action-close-menu').classList.remove('w3-hide');
}
 
function hideMenu() {
	document.getElementById('fm-app-menu').classList.add('w3-hide-small');
	document.getElementById('fm-app-menu').classList.add('w3-hide-medium');
	
	document.getElementById('fm-action-open-menu').classList.remove('w3-hide');
	document.getElementById('fm-action-close-menu').classList.add('w3-hide');
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