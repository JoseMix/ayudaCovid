<template>
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
</template>
<script>
export default {
  name: "HelloWorld",
  props: {
    msg: String,
  },
};
</script>

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
