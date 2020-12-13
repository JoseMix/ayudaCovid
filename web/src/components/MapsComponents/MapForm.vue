<template>
  <div class="mapa">
    <l-map :zoom="zoom" :center="center">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <l-marker
        :key="index"
        ref="markersRef"
        :lat-lng="{ lat: marker.latitud, lng: marker.longitud }"
      >
      </l-marker>
    </l-map>
  </div>
</template>

<script>
//   LTooltip,, LPopup
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
L.Icon.Default.imagePath = "https://unpkg.com/leaflet@1.3.4/dist/images/";

export default {
  name: "MyMap",
  components: {
    "l-map": LMap,
    "l-tile-layer": LTileLayer,
    "l-marker": LMarker,
    // "l-tooltip": LTooltip,
    // "l-popup": LPopup,
  },
  data() {
    return {
      zoom: 14,
      center: { lat: -34.9187, lng: -57.956 },
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      marker: null,
      markerObjects: null,
    };
  },
};
</script>

<style>
li {
  cursor: pointer;
}
.mapa {
  height: 50%;
  margin: 10px;
}
</style>
