<template>
  <v-app style="margin:0px; padding:0px;">
    <title>Paprpapap</title>
    <v-main>
      <v-parallax dark src="./assets/cdc-w9KEokhajKw-unsplash.jpg" height="300">
        <v-row align="center" justify="center">
          <v-col class="text-center" cols="12">
            <h1 class="display-1 font-weight-black mb-4">
              Ayuda Covid
            </h1>
          </v-col>
        </v-row>
      </v-parallax>

      <NavBar> </NavBar>
      <router-view />
      <Footer> </Footer>
    </v-main>
  </v-app>
</template>

<script>
import NavBar from "./components/HomeComponents/NavBar";
import Footer from "./components/HomeComponents/Footer";

export default {
  name: "App",

  components: {
    NavBar,
    Footer,
  },

  data: () => ({
    //
  }),
  created() {
    document.title = "Covid-19";
  },
};
</script>
