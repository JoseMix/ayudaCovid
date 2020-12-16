<template>
  <div class="Estadisticas">
    <h1 class="display-1 font-weight-thin">Estadisticas</h1>
    <Stats></Stats>

    <router-link to="/" class="btn btn-primary">Volver </router-link>
  </div>
</template>

<script>
// @ is an alias to /src
import Stats from "../components/EstadisticasComponents/Inicio.vue";

export default {
  name: "Estadisticas",
  components: {
    Stats,
  },
};
</script>
