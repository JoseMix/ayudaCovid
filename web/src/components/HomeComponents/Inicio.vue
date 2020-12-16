<template>
  <v-container fluid ma-0 pa-0 fill-height grey lighten-4>
    <v-row class="center py-16 my-16" justify="center">
      <v-col>
        <v-hover>
          <template v-slot:default="{ hover }">
            <v-card :elevation="hover ? 17 : 6" class="mx-auto" max-width="360">
              <v-img
                src="https://www.ocyt.org.co/wp-content/uploads/2017/08/img-area-estadistica.jpg"
                height="200px"
              ></v-img>
              <v-card-title>
                <h2>Estadísticas</h2>
              </v-card-title>
              <v-card-text class="text-center">
                Esta sección se basa en la información de los centros de ayuda
                social.
              </v-card-text>
              <br />
              <v-card-actions>
                <v-btn href="/estadisticas" color="info" text>
                  Acceder
                </v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </template>
        </v-hover>
      </v-col>
      <v-col justify="center">
        <v-hover>
          <template v-slot:default="{ hover }">
            <v-card :elevation="hover ? 17 : 6" class="mx-auto" max-width="360">
              <v-img
                src="https://www.publicdomainpictures.net/pictures/100000/nahled/heart-plus.jpg"
                height="200px"
                max-width="300px"
              ></v-img>
              <v-card-title>
                <h2>Agregar centro</h2>
              </v-card-title>
              <v-card-text class="text-center">
                Si conoce de algún centro que no esté cargado, ¡ingrese su
                información! posteriormente se validarán los datos y podrá
                visualizarlo en el mapa.
              </v-card-text>
              <v-card-actions>
                <v-btn href="/carga-centro" color="info" text>
                  Acceder
                </v-btn>
              </v-card-actions>
            </v-card>
          </template>
        </v-hover>
      </v-col>
      <v-col align="center" justify="center">
        <v-hover>
          <template v-slot:default="{ hover }">
            <v-card :elevation="hover ? 17 : 6" class="mx-auto" max-width="360">
              <v-img
                src="https://img.unocero.com/2020/06/google-maps.jpg"
                height="200px"
              ></v-img>
              <v-card-title>
                <h2>Centros</h2>
              </v-card-title>
              <v-card-text class="text-center">
                ¿Deseas localizar algún centro cercano? Busca en el mapa los
                centros
              </v-card-text>
              <br />
              <v-card-actions>
                <v-btn href="/centros" color="info" text>
                  Acceder
                </v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </template>
        </v-hover>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    show: false,
  }),
};
</script>
