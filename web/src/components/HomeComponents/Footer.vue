<template>
  <v-footer dark padless class="justify-center pl-0" inset app>
    <v-card class="flex" flat tile>
      <v-card-title class="blue darken-4">
        <strong class="subheading"
          >Contactanos en nuestras redes sociales!</strong
        >

        <v-spacer></v-spacer>

        <v-btn v-for="icon in icons" :key="icon" class="mx-4" dark icon>
          <v-icon size="24px">
            {{ icon }}
          </v-icon>
        </v-btn>
      </v-card-title>

      <!-- <v-card-text class="py-2 white--text text-center">
        {{ new Date().getFullYear() }} — <strong>Ayuda-Covid</strong>
      </v-card-text> -->
    </v-card>
  </v-footer>
</template>

<script>
export default {
  name: "Footer",
  data: () => ({
    icons: ["mdi-facebook", "mdi-linkedin", "mdi-instagram"],
  }),
};
</script>
