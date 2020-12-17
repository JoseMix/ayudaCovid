<template>
    <div>
        <h3>Donaciones por tipo de centro</h3>
        <ve-histogram :data="chartData" :settings="chartSettings"></ve-histogram>
    </div>
</template>



<script>
    import VeHistogram from'v-charts/lib/histogram.common';
    import axios from "axios";
    export default {
        components: { VeHistogram },
        data () {
        this.chartSettings = {
        yAxisName: ['Donaciones']
        }
        return {
            chartData: {
            columns: ['tipo_centro', 'cantidad'],
            rows: []
            }
        }
    },
    created() {
    axios.get("http://127.0.0.1:5000/api/turnosPorTipo/").then((response) => {
        this.chartData.rows = response.data[0].centros[0];
    })
    }
    }
</script>