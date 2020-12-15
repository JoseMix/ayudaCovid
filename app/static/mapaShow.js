let map;
let marker;
const tileUrl = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";

window.onload = () => {
  "Se dispara cuando el html termine de cargar";
  initializeMap("myMap");
};

const initializeMap = () => {
  let lat = document.getElementById("latitud").value;
  let lng = document.getElementById("longitud").value;

  map = L.map("myMap").setView([lat, lng], 12);
  L.tileLayer(tileUrl).addTo(map);
  marker = L.marker([lat, lng]).addTo(map);
};
