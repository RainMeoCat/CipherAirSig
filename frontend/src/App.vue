<template>
  <div
    class="app"
    :class="$store.getters.returnModeColor"
  >
    <a
      href="https://github.com/RainMeoCat/CipherAirSig"
      class="github-corner"
      target="_blank"
      aria-label="View source on GitHub"
    >
      <svg
        width="120"
        height="120"
        viewBox="0 0 250 250"
        class="octocat"
        aria-hidden="true"
      >
        <path d="M0,0 L115,115 L130,115 L142,142 L250,250 L250,0 Z" />
        <path
          d="M128.3,109.0 C113.8,99.7 119.0,89.6 119.0,89.6 C122.0,82.7 120.5,78.6 120.5,78.6 C119.2,72.0 123.4,76.3 123.4,76.3 C127.3,80.9 125.5,87.3 125.5,87.3 C122.9,97.6 130.6,101.9 134.4,103.2"
          fill="currentColor"
          style="transform-origin: 130px 106px;"
          class="octo-arm"
        />
        <path
          d="M115.0,115.0 C114.9,115.1 118.7,116.5 119.8,115.4 L133.7,101.6 C136.9,99.2 139.9,98.4 142.2,98.6 C133.8,88.0 127.5,74.4 143.8,58.0 C148.5,53.4 154.0,51.2 159.7,51.0 C160.3,49.4 163.2,43.6 171.4,40.1 C171.4,40.1 176.1,42.5 178.8,56.2 C183.1,58.6 187.2,61.8 190.9,65.4 C194.5,69.0 197.7,73.2 200.1,77.6 C213.8,80.2 216.3,84.9 216.3,84.9 C212.7,93.1 206.9,96.0 205.4,96.6 C205.1,102.4 203.0,107.8 198.3,112.5 C181.9,128.9 168.3,122.5 157.7,114.1 C157.9,116.9 156.7,120.9 152.7,124.9 L141.0,136.5 C139.8,137.7 141.6,141.9 141.8,141.8 Z"
          fill="currentColor"
          class="octo-body"
        />
      </svg>
    </a>
    <el-dialog
      v-model="visible"
      :show-close="false"
    >
      <template #header="{ close, titleId, titleClass }">
        <div class="my-header">
          <h1
            :id="titleId"
            :class="titleClass"
            style="font-size:24px"
          >
            CipherAirSig是什麼?
          </h1>
          <el-button
            type="danger"
            :icon="CircleCloseFilled"
            @click="close"
          >
            關閉
          </el-button>
        </div>
      </template>
      <div style="font-size:16px;text-align:left">
        該系統CipherAirSig可以從視覺上捕捉使用者的手部骨架，並應用手勢變化來簽名，本系統規劃了四種手勢，
        四種手勢對應每一個筆畫，依據筆畫順序能產生出一個編碼序列，作為密碼，能夠增加簽名生物認證的安全性，同時也會以筆跡、簽名速度來進行驗證。
        <div style="width:100%;text-align:center">
          <img
            src="@/assets/簽名流程.png"
            style="margin:15px 0px;width:85%"
          >
        </div>
        系統尚在構建中，尚不開放註冊，僅提供預設的兩組簽名/兩組帳號供測試，目前只能在電腦上使用，請使用Chrome/edge瀏覽器，並開啟網頁的攝像頭權限。
      </div>
    </el-dialog>
    <div
      class="code"
    >
      Source Code
    </div>
    <div style="background-color:white;border-radius:10px">
      <div class="nav">
        <h1>
          <el-link
            class="nav-a"
            :underline="false"
            style="font-size:24px;"
            @click="returnHome()"
          >
            CipherAirSig demo
          </el-link>
        </h1>
        <el-link
          class="nav-a"
          :underline="false"
          @click="visible = true"
        >
          這是什麼？
        </el-link> |
        <el-link
          class="nav-a"
          :underline="false"
          @click="enterMode('gesture')"
        >
          登入
        </el-link> |
        <el-tooltip
          class="box-item"
          effect="dark"
          content="尚未開放"
          placement="right"
        >
          <el-link
            class="nav-a"
            :underline="false"
            disabled
            @click="enterMode('gesture')"
          >
            註冊
          </el-link>
        </el-tooltip>
      </div>
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
import { CircleCloseFilled } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ref } from 'vue'
export default {
  name: 'App',
  setup () {
    const router = useRouter()
    const store = useStore()
    const visible = ref(false)
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
      visible,
      enterMode,
      returnHome,
      CircleCloseFilled
    }
  }
}
</script>
<style lang="scss" scoped>
@import "./assets/font.css";
.circles {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  margin: 0px;
  padding: 0px;
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
$circles-size: (80px, 20px, 20px, 60px, 20px, 110px, 150px, 25px, 15px, 150px);
$circles-position: (25%, 10%, 70%, 40%, 65%, 75%, 35%, 50%, 20%, 85%);
$circles-delay: (0s, 2s, 4s, 0s, 0s, 3s, 7s, 15s, 2s, 0s);
$circles-duration: (25s, 12s, 25s, 18s, 25s, 25s, 25s, 25s, 45s, 35s);
@for $i from 1 through 10 {
  $position: nth($circles-position, $i);
  $delay: nth($circles-delay, $i);
  $duration: nth($circles-duration, $i);
  $size: nth($circles-size, $i);
  .circles li:nth-child(#{$i}) {
    left: $position;
    width: $size;
    height: $size;
    animation-delay: $delay;
    animation-duration: $duration;
  }
}
@keyframes animate {
  0% {
    transform: translateY(0) rotate(0deg);
    opacity: 1;
    border-radius: 0;
  }
  100% {
    transform: translateY(-1000px) rotate(720deg);
    opacity: 0;
    border-radius: 50%;
  }
}
.app {
  font-family: "Gen Jyuu Gothic";
  text-align: center;
  color: #2c3e50;
  background: linear-gradient(
    180deg,
    #e1803f,
    #fef2ad,
    #7361e4,
    #f8adfe,
    #3ab25a,
    #adfed1
  );
  background-size: 500% 500%;
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
body {
  margin: 0px;
}
.code {
  rotate: 45deg;
  position: absolute;
  top: 40px;
  right: 10px;
  color: #3e3e3e98;
  mix-blend-mode: color-burn;
  font-weight: bold;
  font-size: 24px;
}
.nav {
  background-color: white;
  padding: 10px 15px;
  filter: drop-shadow(3px 3px 3px rgba(0, 0, 0, 0.5));
  border-radius: 5px;
  color: rgb(85, 85, 85);
  text-align: left;
  position: absolute;
  bottom: 10px;
  left: 10px;
  font-weight: bold;
  z-index: 100;
  h1 {
    margin: 0px;
    font-size: 24px;
  }
  .nav-a {
    color: rgb(85, 85, 85) !important;
    font-weight: bold;
    font-size: 16px;
    transition: all 0.5s cubic-bezier(0.33, 1, 0.68, 1);
    &:hover {
      color: rgb(70, 193, 255) !important;
    }
  }
}
.my-header {
  display: flex;
  align-items: center;
  flex-direction: row;
  justify-content: space-between;
}
.powered {
  mix-blend-mode: color-burn;
  color: rgba(50, 50, 50, 0.75);
  position: absolute;
  width: 100vw;
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

.octocat {
  fill: #3e3e3e98;
  mix-blend-mode: color-burn;
  color: rgb(255, 255, 255);
  position: absolute;
  top: 0;
  border: 0;
  right: 0;
  z-index: 5;
}

.github-corner:hover .octo-arm {
  animation: octocat-wave 560ms ease-in-out;
}

@keyframes octocat-wave {
  0%,
  100% {
    transform: rotate(0);
  }

  20%,
  60% {
    transform: rotate(-25deg);
  }

  40%,
  80% {
    transform: rotate(10deg);
  }
}

@media (max-width: 500px) {
  .github-corner:hover .octo-arm {
    animation: none;
  }

  .github-corner .octo-arm {
    animation: octocat-wave 560ms ease-in-out;
  }
}
</style>
