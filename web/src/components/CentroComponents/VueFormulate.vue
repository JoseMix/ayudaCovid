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
            type="select"
            name="id_municipio"
            label="Municipio"
            :options="municipios"
          />

          <FormulateInput type="submit" label="Enviar" />
        </v-col>
      </v-row>
    </v-container>

    <h5>{{ formValues }}</h5>
  </FormulateForm>
</template>

<script>
import axios from "axios";
export default {
  data: () => {
    return {
      items: ["Comida", "Ropa", "Plasma"],
      formValues: {},
      municipios: {},
      nombre: "",
      direccion: "",
      email: "",
      errors: "",
      phoneNumber: "",
    };
  },
  methods: {
    handleSubmit() {
      axios
        .post("http://127.0.0.1:5000/api/centros/", this.formValues, {
          headers: {},
        })
        .then((result) => {
          console.log(typeof result);
        });
    },
  },
  created() {
    axios
      .get(
        "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?page=1&per_page=140",
        {}
      )
      .then((result) => {
        this.municipios = result.data.data.Town;
        this.municipios = Object.values(this.municipios);
<<<<<<< HEAD
        //this.municipios.forEach((elemento) => {
        this.municipios = JSON.parse(this.municipios);
        //this.nuevinsky[elemento.id] = elemento.name;
        //this.nuevinsky.push({ value: elemento.id, label: elemento.name });
=======
>>>>>>> 6293b5e7bb05570371660e938658cce2cd75807f

        let arr = [];
        this.municipios.forEach((element) => {
          arr.push({ label: element.name, value: `${element.id}` });
        });
        this.municipios = arr;
      });
  },

  nameRules() {
    return true;
  },
  emailRules() {
    return true;
  },
};
</script>
