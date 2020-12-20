<template>
  <v-app style="margin:0px; padding:0px;">
    <v-main v-if="sitio.activo == 1">
      <v-parallax dark src="./assets/cdc-w9KEokhajKw-unsplash.jpg" height="300">
        <v-row align="center" justify="center">
          <v-col class="text-center" cols="12">
            <h1 class="display-1 font-weight-black mb-4">
              {{ sitio.titulo }}
            </h1>
          </v-col>
        </v-row>
      </v-parallax>

      <NavBar> </NavBar>
      <router-view />
      <Footer> </Footer>
    </v-main>
    <v-main v-if="sitio.activo == 0">
      <v-container
        fluid
        ma-0
        px-6
        fill-height
        class="indigo lighten-1 white--text"
      >
        <v-row>
          <v-col>
            <h1 class="display-1 font-weight-light" style="text-align:center">
              {{ sitio.titulo }} se encuentra deshabilitado
            </h1>
          </v-col>
        </v-row>
        <v-row>
          <v-col style="text-align:center">
            <v-btn
              class="success"
              href="https://admin-grupo13.proyecto2020.linti.unlp.edu.ar/iniciar_sesion"
              >Log In</v-btn
            >
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import NavBar from "./components/HomeComponents/NavBar";
import Footer from "./components/HomeComponents/Footer";
import axios from "axios";

export default {
  name: "App",

  components: {
    NavBar,
    Footer,
  },

  data: () => ({
    sitio: [],
    //
  }),
  created() {
    document.title = "Covid-19";
    axios
      .get("https://admin-grupo13.proyecto2020.linti.unlp.edu.ar/api/sitio/")
      .then((response) => {
        console.log(typeof response.data[0].sitio);
        this.sitio = response.data[0].sitio;
        console.log(this.sitio.titulo);
        // "http://127.0.0.1:5000/api/sitio/"
      });
  },
};
</script>
