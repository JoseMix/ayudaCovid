<template>
  <div class="Carga_centro">
    <UploadComponent></UploadComponent>
    <h1>Alta de centro</h1>
    <p>
      Formulario para solicitud de centro en proceso.
    </p>

    <router-link to="/" class="btn btn-primary">Volver </router-link>
  </div>
</template>

<script>
// @ is an alias to /src
import UploadComponent from "../components/CentroComponents/UploadComponent.vue";

export default {
  name: "Carga_centro",
  components: {
    UploadComponent,
  },
};
</script>
