<template>
  <div class="app">
    <ul class="circles">
      <li
        v-for="n in 10"
        :key="n"
      />
    </ul>
    <router-view />
  </div>
</template>

<style lang="scss" scoped>
@import "./assets/font.css";
.circles{
  position: absolute;
  top: 0;
  left: 0;
  z-index:0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  margin:0px;
  padding:0px;
  li {
    position: absolute;
    display: block;
    list-style: none;
    width: 20px;
    height: 20px;
    background: rgba(255, 255, 255, 0.2);
    animation: animate 25s linear infinite;
    bottom: -150px;
  }
}
$circles-size: (80px,20px,20px,60px,20px,110px,150px,25px,15px,150px);
$circles-position: (25%,10%,70%,40%,65%,75%,35%,50%,20%,85%);
$circles-delay: (0s,2s,4s,0s,0s,3s,7s,15s,2s,0s);
$circles-duration: (25s,12s,25s,18s,25s,25s,25s,25s,45s,35s);
@for $i from 1 through 10 {
  $position: nth($circles-position, $i);
  $delay: nth($circles-delay, $i);
  $duration: nth($circles-duration, $i);
  $size: nth($circles-size, $i);
  .circles li:nth-child(#{$i}){
    left: $position;
    width: $size;
    height: $size;
    animation-delay: $delay;
    animation-duration: $duration
  }
}
@keyframes animate {
  0%{
    transform: translateY(0) rotate(0deg);
    opacity: 1;
    border-radius: 0;
  }
  100%{
    transform: translateY(-1000px) rotate(720deg);
    opacity: 0;
    border-radius: 50%;
  }
}
.app {
  font-family: "Gen Jyuu Gothic";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  background: linear-gradient(#7361E4, #F8ADFE);height: 100vh;width: 100vw;
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
