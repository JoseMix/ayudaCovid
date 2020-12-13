<template>
  <div class="home">
    <!-- <NavBar></NavBar> lo puse en App porque es algo que se repite para todas las vistas-->
    <HelloWorld></HelloWorld>
  </div>
</template>

<script>
// @ is an alias to /src
// import NavBar from "@/components/HomeComponents/NavBar.vue";
import HelloWorld from "../components/HomeComponents/HelloWorld.vue";

export default {
  name: "Home",
  components: {
    // NavBar,
    HelloWorld,
  },
};
</script>
