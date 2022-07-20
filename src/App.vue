<template>
  <div
    class="app"
    :class="$store.getters.returnModeColor"
  >
    <transition
      name="el-fade-in"
      appear
    >
      <div
        :key="$store.state.signMode"
        class="mode"
      >
        {{ $store.state.signMode }}
      </div>
    </transition>
    <div class="nav">
      <h1>
        <el-link
          class="nav-a"
          :underline="false"
          style="font-size:24px;"
          @click="returnHome()"
        >
          ITALAB 2022 thesis demo
        </el-link>
      </h1>
      <el-link
        class="nav-a"
        :underline="false"
        @click="enterMode('gesture')"
      >
        gesture
      </el-link>  /  <el-link
        class="nav-a"
        :underline="false"
        @click="enterMode('hash')"
      >
        hash
      </el-link>
    </div>
    <div class="powered">
      Powered by <img
        src="@/assets/MPlogo.png"
        style="width:16px;filter: grayscale(100%) brightness(0.6) opacity(1);vertical-align:text-top"
      >Mediapipe.
    </div>
    <ul class="circles">
      <li
        v-for="n in 10"
        :key="n"
      />
    </ul>
    <router-view v-slot="{ Component, route }">
      <transition name="fade">
        <component
          :is="Component"
          :key="route.path"
        />
      </transition>
    </router-view>
  </div>
</template>
<script>
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
export default {
  name: 'App',
  setup () {
    const router = useRouter()
    const store = useStore()
    function returnHome () {
      store.commit('resetSign')
      store.commit('changeMode', '')
      router.push('/')
    }
    function enterMode (mode) {
      store.commit('resetSign')
      store.commit('changeMode', mode)
      router.push('/login')
    }
    return {
      enterMode,
      returnHome
    }
  }
}
</script>
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
  text-align: center;
  color: #2c3e50;
  background: linear-gradient(180deg, #e1803f, #fef2ad, #7361E4, #F8ADFE, #3ab25a, #adfed1);
  background-size:500% 500%;
  height: 100vh;
  width: 100vw;
  background-position: 0% 0%;
  transition: all 1s cubic-bezier(0.33, 1, 0.68, 1);
}
.gesture {
  background-position: 0% 50%;
  transition: all 1s cubic-bezier(0.33, 1, 0.68, 1);
}
.hash {
  background-position: 0% 100%;
  transition: all 1s cubic-bezier(0.33, 1, 0.68, 1);
}
body{
  margin:0px;
}
.mode{
  position:absolute;
  top:10px;
  right:10px;
  color:rgba(255,255,255,0.5);
  font-weight: bold;
  font-size:24px
}
.nav {
  mix-blend-mode: color-burn;
  text-align:left;
  position:absolute;
  bottom:10px;
  left:10px;
  color: rgba(50, 50, 50, 0.3);
  font-weight: bold;
  z-index: 999;
  h1{
    margin:0px;
    font-size:24px;
  }
  .nav-a {
    color: rgba(50, 50, 50, 0.5);
    font-weight: bold;
    transition: all 0.5s cubic-bezier(0.33, 1, 0.68, 1);
    &:hover {
      color: rgba(0, 255, 247, 0.5);
    }
  }
}
.powered{
  mix-blend-mode: color-burn;
  color:rgba(50, 50, 50, 0.75);
  position: absolute;
  width:100vw;
  font-size: 12px;
  bottom: 0px;
  margin-bottom: 5px;
  font-weight: bold;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
  position: absolute;
  width: 100%;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
