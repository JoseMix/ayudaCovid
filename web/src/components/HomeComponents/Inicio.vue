<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card class="mx-auto" max-width="360">
          <v-img
            src="https://www.ocyt.org.co/wp-content/uploads/2017/08/img-area-estadistica.jpg"
            height="200px"
          ></v-img>

          <v-card-title>
            <h2>Estadísticas</h2>
          </v-card-title>

          <v-card-text>
            <p>
              Esta sección se basa en la información de los centros de ayuda
              social.
            </p>
          </v-card-text>
          <br />
          <v-card-actions>
            <v-btn href="#" color="info" text>
              Acceder
            </v-btn>

            <v-spacer></v-spacer>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col>
        <v-card class="mx-auto" max-width="360">
          <v-img
            src="https://www.publicdomainpictures.net/pictures/100000/nahled/heart-plus.jpg"
            height="200px"
            max-width="300px"
          ></v-img>

          <v-card-title>
            <h2>Agregar centro</h2>
          </v-card-title>

          <v-card-text>
            <p>
              Si conoce de algún centro que no esté cargado, ¡ingrese su
              información! posteriormente se validarán los datos y podrá
              visualizarlo en el mapa.
            </p>
          </v-card-text>

          <v-card-actions>
            <v-btn href="/carga-centro" color="info" text>
              Acceder
            </v-btn>

            <v-spacer></v-spacer>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col>
        <v-card class="mx-auto" max-width="360">
          <v-img
            src="https://img.unocero.com/2020/06/google-maps.jpg"
            height="200px"
          ></v-img>

          <v-card-title>
            <h2>Centros</h2>
          </v-card-title>

          <v-card-text>
            <p>
              ¿Deseas localizar algún centro?
            </p>
          </v-card-text>

          <v-card-actions>
            <v-btn href="/centros" color="info" text>
              Acceder
            </v-btn>

            <v-spacer></v-spacer>
          </v-card-actions>
        </v-card>
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

<!--<template>
  <div>
    <div style="display:inline-block">
      <b-card
        title="Estadísticas"
        img-src="https://www.ocyt.org.co/wp-content/uploads/2017/08/img-area-estadistica.jpg"
        img-alt="Image"
        img-top
        tag="article"
        style="max-width: 25rem;"
        class="mb-2"
      >
        <b-card-text>
          Esta sección se basa en la información de los centros de ayuda social.
          <br /><br /><br />
        </b-card-text>
        <router-link to="#" class="btn btn-primary"
          >Ver estadisticas
        </router-link>
      </b-card>
    </div>
    <div style="display:inline-block; margin-left:15px; margin-right:15px;">
      <b-card
        title="Agregar centro"
        img-src="https://www.publicdomainpictures.net/pictures/100000/nahled/heart-plus.jpg"
        img-alt="Image"
        img-top
        tag="article"
        style="max-width: 25rem;"
        class="mb-2"
      >
        <b-card-text>
          Si conoce de algún centro que no esté cargado, ¡ingrese su
          información! posteriormente se validarán los datos y podrá
          visualizarlo en el mapa.
        </b-card-text>
        <router-link to="/carga-centro" class="btn btn-primary"
          >Agregar centro
        </router-link>
      </b-card>
    </div>
    <div style="display:inline-block">
      <b-card
        title="Centros"
        img-src="https://img.unocero.com/2020/06/google-maps.jpg"
        img-alt="Image"
        img-top
        tag="article"
        style="max-width: 25rem;"
        class="mb-2"
      >
        <b-card-text>
          ¿Deseas localizar algún centro?
          <br /><br /><br /><br />
        </b-card-text>

        <router-link to="/centros" class="btn btn-primary"
          >centros
        </router-link>
      </b-card>
    </div>
  </div>
</template>-->

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
