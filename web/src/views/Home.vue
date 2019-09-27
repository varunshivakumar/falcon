<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <HelloWorld msg="Welcome" />

    hello, world
    {{ info }}
    hello, world
    <br/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from "@/components/HelloWorld.vue";
import axios from 'axios'

export default {
  name: "home",
  components: {
    HelloWorld
  },
  data() {
    return {
      test_info: null,
      info: null

    };
  },
  mounted() {
    axios
      .get("https://api.coindesk.com/v1/bpi/currentprice.json")
      .then(response => (this.test_info = response));

    axios
      .get("http://localhost:8080/api/items")
      .then(response => this.info = response)
  }
};
</script>
