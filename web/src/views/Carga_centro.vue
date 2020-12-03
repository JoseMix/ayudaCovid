<template>
  <div class="Carga_centro">
    <h1>Alta de centro</h1>
    <VueFormulate></VueFormulate>

    <router-link to="/" class="btn btn-primary">Volver </router-link>
  </div>
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
