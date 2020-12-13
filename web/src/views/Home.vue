<template>
  <v-container>
    <div class="home">
      <Inicio></Inicio>
    </div>
  </v-container>
</template>

<script>
// @ is an alias to /src
import Inicio from "../components/HomeComponents/Inicio";

export default {
  name: "Home",
  components: {
    Inicio,
  },
};
</script>
