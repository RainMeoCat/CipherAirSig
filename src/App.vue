<template>
  <div class="app">
    <router-view />
  </div>
</template>

<style lang="scss" scoped>
@import "./assets/font.css";
.app {
  font-family: "Gen Jyuu Gothic";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
body{
  margin:0px;
}
nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
