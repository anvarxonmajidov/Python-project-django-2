<template>
  <div>
    <Nav/>
    <router-view/>
    <Footer/>
  </div>
</template>
<script>
import axios from 'axios';

import Nav from '@/components/Nav'
import Footer from '@/components/Footer'
export default {
  name: 'App',
  components: {
    Nav,
    Footer
  },
  beforeCreate() {
    console.log('beforeCreate');
    this.$store.commit('initializeStore');

    const token=this.$store.state.user.token;

    if(token){
      axios.defaults.headers.common['Authorization']="Token "+token;
    }else{
      axios.defaults.headers.common['Authorization']=""
    }
  }
  // watch: {
  //   "$route.path"(value) {
  //     console.log(value);
  //   }
  // }
}
</script>
<style lang="scss">
@import '../node_modules/bulma';

</style>
// 192.168.137.150,saulgadgets.com