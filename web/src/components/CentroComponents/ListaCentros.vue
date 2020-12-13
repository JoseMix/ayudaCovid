<template>
  <v-container>
    <v-layout row wrap>
      <v-flex xs12 sm6>
        <v-card>
          <v-card-title>Centros</v-card-title>
          <v-card-text>
            <v-list v-for="centro in centros" :key="centro.id">
              <v-list-item>{{ centro.nombre }} | {{ centro.web }} </v-list-item>
              <v-list-item
                ><FormulateForm v-model="formValues">
                  <FormulateInput
                    name="fecha"
                    label="Fecha"
                    type="date"
                    validation="required"
                  />
                  <h3>{{ formValues.fecha }}</h3>
                </FormulateForm></v-list-item
              >
              <v-list-item
                ><router-link
                  :to="{
                    name: 'Turnos',
                    params: { id: centro.id, fecha: formValues.fecha },
                  }"
                >
                  <v-btn depressed color="primary"
                    >Sacar Turno</v-btn
                  ></router-link
                ></v-list-item
              >
            </v-list>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>
<script>
import axios from "axios";
export default {
  data: () => ({
    centros: null,
    formValues: {},
  }),
  mounted: function() {
    //axios.get('http://127.0.0.1:5000/api/centros/').then(response =>console.log(response.data[0].centros[0][0].nombre))
    axios
      .get("http://127.0.0.1:5000/api/centros/")
      .then((response) => (this.centros = response.data[0].centros[0]));
  },
};
</script>
