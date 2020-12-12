<template>
  <v-container >
    <v-layout row wrap  > {{ horarios() }} 
    <v-flex  xs12 sm6 >
    <v-card >
      <v-card-title>Centros</v-card-title>
      <v-card-text>
      <v-list v-for="centro in centros" :key="centro.id">    
      <v-list-item>{{ centro.nombre }} | {{ centro.web }} |  </v-list-item>
      <v-list-item><FormulateForm v-model="formValues">
        <FormulateInput
          name="fecha"
          label="Fecha"
          type="date"
          validation="required"
          :min="fecha_ini"
          :max="fecha_fin" 
        />        
      </FormulateForm></v-list-item>
      <v-list-item><router-link  :to="{ name:'Turnos', params: {id: centro.id, fecha: formValues.fecha} }" >
      <v-btn depressed color="primary">Sacar Turno</v-btn></router-link></v-list-item>
        </v-list>
        </v-card-text>
        </v-card>
        </v-flex>
      
  </v-layout>
  </v-container>
</template>
<script>
import axios from "axios";
import moment from "moment"; 
//this.hora_fin = moment("2016-03-12 "+this.hora_inicio+":00").add(30, 'minutes').format('HH:mm');
export default {
  data: () => ({
    centros: null,
    formValues: {},
    fecha_fin:null,
    fecha_ini:null,
    date: null,
  }),
  methods:{
    horarios(){
      this.fecha_ini =  moment().format("YYYY[-]M[-]D"); 
      console.log("hoy",this.fecha_ini);
      this.fecha_fin = moment("2020-12-12"+ " 00:00:00").add(3, 'days').format("YYYY[-]M[-]D"); 
      console.log("3 dias",this.fecha_fin);

    },
    methods: {
      allowedDates: val => parseInt(val.split('-')[1], 10) % 2 === 0,
    },
  },
  mounted: function() {
    //axios.get('http://127.0.0.1:5000/api/centros/').then(response =>console.log(response.data[0].centros[0][0].nombre))
    axios
      .get("http://127.0.0.1:5000/api/centros/")
      .then((response) => (this.centros = response.data[0].centros[0]));
  },
};
</script>
