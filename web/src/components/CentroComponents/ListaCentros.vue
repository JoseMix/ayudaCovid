<template>
    <div>
        <h1>Centros</h1>
        
        <v-list v-for="centro in centros" :key="centro.id" > 
                <v-list-item>{{ centro.nombre }} | {{centro.web}} </v-list-item>
                <router-link  :to="{ name:'Turnos', params: {nombre: centro.nombre} }" class="btn btn-primary">Sacar Turno</router-link> -->
        </v-list>       

    </div>
</template>
<script>
import axios from "axios";
export default {
    data: () => ({
        centros: null,
    }),
    mounted: function () {
        //axios.get('http://127.0.0.1:5000/api/centros/').then(response =>console.log(response.data[0].centros[0][0].nombre))
        axios.get('http://127.0.0.1:5000/api/centros/').then(response => this.centros = response.data[0].centros[0])
    }

}
</script> 