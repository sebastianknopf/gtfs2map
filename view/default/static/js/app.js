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

function initFeedMap(mapContainerId) {
	const map = new maplibregl.Map({
		container: mapContainerId,
		style: 'https://tiles.openfreemap.org/styles/positron',
		center: [8.5466048, 48.888177],
		zoom: 14
	});
}