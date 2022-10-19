<template>
  <div
    class="app"
    :class="$store.getters.returnModeColor"
  >
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
            這是什麼?
          </h1>
          <el-button
            type="danger"
            :icon="CircleCloseFilled"
            @click="close"
          >
            Close
          </el-button>
        </div>
      </template>
      <div style="font-size:16px;text-align:left">
        該網頁系統可以從視覺上捕捉使用者的手部骨架，並應用手勢變化來簽名，本系統規劃了四種手勢，
        四種手勢對應每一個筆畫，依據筆畫順序能產生出一個編碼序列，作為密碼，能夠增加簽名生物認證的安全性，同時也會以筆跡、簽名速度來進行驗證。
        <img
          src="@/assets/簽名流程.png"
          style="margin:15px 0px;width:100%"
        >
        系統尚在構建中，尚不開放註冊，僅提供預設的兩組簽名/兩組帳號供測試，目前只能在電腦上使用，請使用Chrome/edge瀏覽器，並開啟網頁的攝像頭權限。
      </div>
    </el-dialog>
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
.mode {
  position: absolute;
  top: 10px;
  right: 10px;
  color: rgba(255, 255, 255, 0.5);
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
</style>
