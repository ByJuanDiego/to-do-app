<script>
export default {
  data() {
    return {
      username: ""
    }
  }
}
</script>

<template>
  <div class="about">
    <h3>Introduce your username</h3>
    <input placeholder="username" v-model="username">
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>

