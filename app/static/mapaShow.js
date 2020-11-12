let map;
let marker;
const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

window.onload = () => {
    'Se dispara cuando el html termine de cargar'
    initializeMap('myMap');
};

const initializeMap = ({lat,lng}) => {
    map = L.map('myMap').setView([-34.9187,-57.956], 13);
    L.tileLayer(tileUrl).addTo(map);
    marker = L.marker([lat, lng]).addTo(map);
};
