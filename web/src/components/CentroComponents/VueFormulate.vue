<template>
  <FormulateForm v-model="formValues" @submit="handleSubmit">
    <v-container>
      <v-row>
        <v-col>
          <h2>Formulario centros</h2>

          <FormulateInput name="nombre" label="nombre" validation="required" />
          <FormulateInput
            name="direccion"
            label="direccion"
            validation="required"
          />
          <FormulateInput
            name="apertura"
            label="apertura"
            type="time"
            validation="required"
          />
          <FormulateInput
            name="cierre"
            label="cierre"
            type="time"
            validation="required"
          />

          <FormulateInput
            name="email"
            label="email"
            type="email"
            validation="required"
          />
        </v-col>
        <v-col>
          <FormulateInput name="latitud" label="latitud" />
          <FormulateInput name="longitud" label="longitud" />
          <FormulateInput
            name="telefono"
            label="telefono"
            type="number"
            validation="required"
          />
          <FormulateInput
            name="tipo_centro"
            label="tipo de centro"
            type="select"
            :options="{ Ropa: 'ropa', Plasma: 'plasma', Comida: 'comida' }"
            validation="required"
          />
          <FormulateInput
            name="web"
            label="web"
            type="url"
            validation="required"
          />
          <FormulateInput
            name="id_municipio"
            label="id_municipio"
            type="select"
            :options="options"
          />

          <FormulateInput type="submit" label="Enviar" />
        </v-col>
      </v-row>
    </v-container>
    <h3>{{ formValues }}</h3>
  </FormulateForm>
</template>

<script>
import axios from "axios";
export default {
  data: () => ({
    formValues: {},
    value: [],
    options: [],
  }),
  methods: {
    handleSubmit() {
      axios
        .post("http://127.0.0.1:5000/api/centros/", this.formValues, {
          headers: {},
        })
        .then((result) => {
          console.log(result);
        });
    },
  },
  mounted() {
    axios
      .get(
        "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?per_page=135"
      )
      .then((result) => {
        this.options = result.data["data"]["Town"];
        this.options.map((muni) => console.log(muni));
      });
  },
};
</script>
