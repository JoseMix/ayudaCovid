<template>
  <v-app-bar app class="white--text blue darken-4">
    <v-toolbar-title>
      <router-link to="/">
        <v-btn color="white" text rounded class="my-2">
          <h2>Donaciones - Covid 19</h2>
        </v-btn>
      </router-link>
    </v-toolbar-title>

    <v-row no-gutters>
      <router-link to="/estadisticas">
        <v-btn color="white" text rounded class="my-2">
          Estadísticas
        </v-btn>
      </router-link>

      <router-link to="/carga-centro">
        <v-btn color="white" text rounded class="my-2">
          Agregar centro
        </v-btn>
      </router-link>

      <router-link to="/centros">
        <v-btn color="white" text rounded class="my-2">
          Ver centros
        </v-btn>
      </router-link>
    </v-row>

    <v-spacer></v-spacer>

    <v-btn
      class="success"
      href="https://admin-grupo13.proyecto2020.linti.unlp.edu.ar/iniciar_sesion"
      >Log In</v-btn
    >
  </v-app-bar>
</template>

<script>
export default {
  name: "NavBar",
  data: () => ({}),
};
</script>
