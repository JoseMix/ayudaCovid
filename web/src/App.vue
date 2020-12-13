<template>
  <v-app>
    <v-main>
      <NavBar> </NavBar>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import NavBar from "./components/HomeComponents/NavBar";
export default {
  name: "App",

  components: {
    NavBar,
  },

  data: () => ({
    //
  }),
};
</script>
