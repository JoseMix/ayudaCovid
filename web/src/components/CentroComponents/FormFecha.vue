<template>
  <v-container >
    {{ horarios() }} 
      <FormulateForm v-model="formValues">
        <FormulateInput
          name="fecha"
          label="Fecha"
          type="date"
          validation="required"
          :min="fecha_ini"
          :max="fecha_fin" 
        />        
      </FormulateForm>
      <router-link  :to="{ name:'Turnos', params: {id: 1, fecha: formValues.fecha} }" >
      <v-btn depressed color="primary">Sacar Turno</v-btn></router-link>
  </v-container>
</template>

<script>
import moment from "moment"; 
export default {
  data: () => ({

    formValues: {},
    fecha_fin:null,
    fecha_ini:null,
  }),
  methods:{
    horarios(){
      this.fecha_ini =  moment().format("YYYY[-]M[-]D"); 
      this.fecha_fin = moment("2020-12-12"+ " 00:00:00").add(3, 'days').format("YYYY[-]M[-]D"); 
      
    },
  },

};
</script>
