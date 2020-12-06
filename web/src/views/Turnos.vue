<template>
  <div class="Turnos">
    <h1>Página de Turnos</h1>
    <h2>{{ $route.params.nombre }}</h2>
    <h2>{{ $route.params.fecha }}</h2>
    <FormularioTurnos/>
    <router-link to="/centros" class="btn btn-primary">Volver </router-link>
  </div>
</template>
<script>
import FormularioTurnos from "../components/TurnoComponents/FormularioTurnos.vue";
export default {
  name: "Turnos",
  components: {
    FormularioTurnos,
  },
};
</script>
