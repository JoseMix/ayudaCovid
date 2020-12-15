<template>
  <div class="mapa">
    <l-map :zoom="zoom" :center="center" @click="addMarker">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <l-marker ref="markersRef" :lat-lng="{ lat: latitud, lng: longitud }">
      </l-marker>
    </l-map>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

L.Icon.Default.imagePath = "https://unpkg.com/leaflet@1.3.4/dist/images/";

export default {
  name: "MapComponent",
  components: {
    "l-map": LMap,
    "l-tile-layer": LTileLayer,
    "l-marker": LMarker,
  },
  data() {
    return {
      zoom: 14,
      center: { lat: -34.9187, lng: -57.956 },
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      latitud: null,
      longitud: null,
    };
  },
  methods: {
    addMarker(event) {
      this.latitud = event.latlng.lat;
      this.longitud = event.latlng.lng;
      this.act();
    },
    act() {
      this.$emit("latitud", this.latitud);
      this.$emit("longitud", this.longitud);
    },
  },
};
</script>

<style>
li {
  cursor: pointer;
}
.mapa {
  position: sticky;
  height: 100%;
  width: 100%;
}
</style>
