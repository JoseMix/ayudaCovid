<template>
  <div>
    <FormulateForm v-model="formValues" @submit="llamarAlOtroCOmponente">
      <v-container>
        <v-row>
          <v-col>
            <h2>Formulario Turnos</h2>
            <FormulateInput
              name="hora"
              label="Hora"
              type="time"
              validation="required"
            />
            <FormulateInput
              name="email"
              label="Email"
              type="text"
              validation="required"
            />
            <FormulateInput
              name="telefono"
              label="Telefono"
              type="text"
              validation="required"
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
  data: () => ({
    centros: null,
  }),
  mounted: function() {
    //axios.get('http://127.0.0.1:5000/api/centros/').then(response =>console.log(response.data[0].centros[0][0].nombre))
    axios
      .get("https://admin-grupo13.proyecto2020.linti.unlp.edu.ar/api/centros/")
      .then((response) => (this.centros = response.data[0].centros[0]));
    //http://127.0.0.1:5000/api/centros/<int:centro_id>/turnos_disponibles/?fecha=<fecha>
  },
};
</script>
