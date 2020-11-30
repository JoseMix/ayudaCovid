<template>
  <div class="home">
    <NavBar></NavBar>
    <HelloWorld></HelloWorld>
  </div>
</template>

<script>
// @ is an alias to /src
import NavBar from "@/components/HomeComponents/NavBar.vue";
import HelloWorld from "../components/HomeComponents/HelloWorld.vue";

export default {
  name: "Home",
  components: {
    NavBar,
    HelloWorld,
  },
};
</script>
