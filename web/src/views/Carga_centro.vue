<template>
  <v-container>
    <h1 class="display-1 font-weight-thin" style="text-align:center">
      Creación de solicitud de centro
    </h1>
    <VueFormulate></VueFormulate>
  </v-container>
</template>

<script>
// @ is an alias to /src
import VueFormulate from "../components/CentroComponents/VueFormulate.vue";

export default {
  name: "Carga_centro",
  components: {
    VueFormulate,
  },
};
</script>
