<template>
  <v-container>
    <h1 class="display-1 font-weight-thin" style="text-align:center">
      Mapa de Centros
    </h1>
    <MyMap />
    <br />
  </v-container>
</template>

<script>
import MyMap from "../components/MapsComponents/MyMaps.vue";

export default {
  name: "Centros",
  components: {
    MyMap,
  },
};
</script>

<style>
html,
body,
#app,
div.container {
  height: 100%;
  margin: 0;
}
</style>
