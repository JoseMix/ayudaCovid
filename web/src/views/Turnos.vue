<template>
  <div class="Turnos">
    <h1>Página de Turnos</h1>

    <h3>{{ urlApi($route.params.id, $route.params.fecha) }}</h3>

    <router-link to="/centros" class="btn btn-primary">Volver </router-link>
    <FormulateForm v-model="formValues" @submit="llamarAlOtroCOmponente">
      <v-container>
        <v-row>
          <v-col>
            <h2>Formulario Turnos</h2>
            <FormulateInput
              name="email"
              label="Email"
              type="text"
              validation="required"
            />
            <FormulateInput
              name="nombre"
              label="Nombre"
              type="text"
              validation="required"
            />
            <FormulateInput
              name="apellido"
              label="Hora"
              type="text"
              validation="required"
            />
            <FormulateInput
              name="telefono"
              label="Telefono"
              type="text"
              validation="required"
            />
            <FormulateInput
              name="hora"
              label="hora"
              type="select"
              :options="options"
            />
            <FormulateInput type="submit" label="Enviar" />
          </v-col>
        </v-row>
      </v-container>
      <h3>{{ formValues }}</h3>
    </FormulateForm>
  </div>
</template>
<script>
import axios from "axios";
export default {
  name: "Turnos",
  components: {},
  data: () => ({
    turnos: null,
    options: [],
    fecha: null,
    url: null,
  }),
  methods: {
    urlApi(id, fecha) {
      this.fecha = fecha
        .split("-")
        .reverse()
        .join("-");
      this.url =
        "http://127.0.0.1:5000/api/centros/" +
        id +
        "/turnos_disponibles/?fecha=" +
        this.fecha;
    },
  },
  mounted: function() {
    /*axios
      .get(this.url)
      .then((response) => console.log(response.data[0].turno.all));*/
    axios
      .get(this.url)
      .then((result) => (this.options = result.data[0].turno[0]));
  },
};
</script>
