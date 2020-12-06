<template>
  <div class="Turnos">
    <h1>Página de Turnos</h1>
    <h2> {{ $route.params.id }} </h2>
    <h2> {{ $route.params.fecha.split('-').reverse().join('-') }} </h2>
    
    <router-link to="/centros" class="btn btn-primary">Volver </router-link>
    <FormulateForm v-model="formValues" @submit="llamarAlOtroCOmponente">
        <v-container>
        <v-row>
        <v-col>
        <h2>Formulario Turnos</h2>
          <FormulateInput name="email" label="Email" type="text" validation="required"/>
          <FormulateInput name="nombre" label="Nombre" type="text" validation="required"/>
          <FormulateInput name="apellido"  label="Hora"  type="text" validation="required"/>
          <FormulateInput name="telefono" label="Telefono" type="text" validation="required"/>
          <FormulateInput name="hora" label="hora" type="select" :options="options"/>    
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
  components: {    
  },
 data: () => ({
        turnos: null,
        options: [],
    }),
    mounted: function () {
        //axios.get('http://127.0.0.1:5000/api/centros/1/turnos_disponibles/?fecha=08-12-2020').then(response => console.log(response.data[0].turno))    
        axios.get('http://127.0.0.1:5000/api/centros/1/turnos_disponibles/?fecha=08-12-2020').then((result) => this.options = result.data[0].turno[0]);
   }
}

</script>
