<template>
  <div
    class="container"
    :class="{ 'progress': isHoldOver1Point5Sec}"
  >
    <transition
      name="el-fade-in"
      appear
    >
      <div
        :key="signState"
        class="stat"
      >
        {{ signState }}
      </div>
    </transition>
    <div class="capture-info">
      FPS：{{ fps }}<br>
      與食指距離：{{ handDist.index }}<br>
      與中指距離：{{ handDist.middle }}<br>
      與無名指距離：{{ handDist.ring }}<br>
      與小指距離：{{ handDist.pinky }}<br>
      手部偵測狀態：{{ handDetected }}<br>
      手部靜止狀態：{{ ifHold }}<br>
    </div>
    <div class="sig-info">
      <img
        :src="$store.state.sigPic"
        style="height:100%"
      >
    </div>
    <video
      ref="hiddenCamera"
      style="display:none;width:70vw;height:60vh"
    />
    <div class="canvas-container">
      <transition
        name="el-zoom-in-center"
        style="position:relative"
      >
        <div v-show="cameraShow">
          <div class="sign-option">
            <el-button
              type="danger"
              :icon="Delete"
              round
              size="large"
              @click="$store.commit('resetSign')"
            >
              重新繪製
            </el-button>
          </div>
          <canvas
            ref="outputCanvas"
            class="output-canvas"
            :width="width"
            :height="height"
          />
        </div>
      </transition>
      <transition
        name="el-zoom-in-center"
        @after-leave="loadingLeave"
      >
        <div
          v-show="loadingShow"
          class="loading"
        >
          載入中...
        </div>
      </transition>
    </div>
  </div>
</template>
<script>
import { Delete } from '@element-plus/icons-vue'
import { useStore } from 'vuex'
import 'element-plus/theme-chalk/src/message.scss'
import 'element-plus/theme-chalk/src/index.scss'
import { ref, computed, onMounted, reactive, watch } from 'vue'
import { ElNotification } from 'element-plus'
import { Hands, VERSION } from '@mediapipe/hands'
import { Camera } from '@mediapipe/camera_utils'
import useSignCapture from '@/composables/useSignCapture'
export default {
  name: '2FAPage',
  setup () {
    const store = useStore()
    // 是否偵測到手部，detected：boolean，主要操控這個變數；
    // handDetected：computed，監聽detected變數輸出DOM內容
    const detected = ref(false)
    const handDetected = computed(() => {
      if (detected.value) {
        return '已偵測到手部'
      } else {
        return '未偵測到手部'
      }
    })
    // v-show:兩個元素，loading和canvas，
    // 這兩個變數用於mediapipe載入完成後切換載入畫面和
    const cameraShow = ref(false)
    const loadingShow = ref(true)
    // canvas繪圖用(context)
    const ctx = ref(null)
    // canvas寬和高
    const width = ref(null)
    const height = ref(null)
    // 獲取：網路攝影機（隱藏）與cnavas DOM
    const hiddenCamera = ref(null)
    const outputCanvas = ref(null)
    // 顯示fps
    const fps = ref(1)
    const times = []
    // RGB動畫用步長
    let angleA = Math.random() * 360
    const stepA = 2.5
    // 暫存捕捉到的手部座標點
    // curr和prev兩個座標資訊，curr：現在的，prev：上一組 這裡用來傳給ifhold來檢測靜止狀態
    const landmarks = reactive({
      curr: [],
      prev: []
    })
    // 靜止秒數
    const holdSecond = ref(0)
    // 靜止進度判定超過1.5秒：boolean，主要操控這個變數
    const isHoldOver1Point5Sec = ref(false)
    // 載入簽名筆記捕捉組件
    // handDist：computed，回傳大拇指與其他四指的距離
    // signProcess：主要簽名處理，每一幀手部檢測出來時會傳到這裡
    // ifHold：computed，手部是否靜止，檢測傳過來的landmarks，回傳DOM內容
    // drawSign：簽名繪圖，這裡放在mediapipe的區塊裡，可以逐幀繪製
    const { handDist, signProcess, ifHold, drawSign } = useSignCapture(
      landmarks,
      detected
    )
    // 界面狀態紀錄與送出訊息框
    const signState = ref('開始簽名')
    // inputVideo為網路攝影機的DOM
    const inputVideo = computed(() => {
      return hiddenCamera.value
    })
    // 初始化
    function init () {
      // 載入hands檔案
      const hands = new Hands({
        locateFile: (file) => {
          return `https://cdn.jsdelivr.net/npm/@mediapipe/hands@${VERSION}/${file}`
        }
      })
      // 設定hands參數
      hands.setOptions({
        modelComplexity: 1,
        maxNumHands: 1,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5
      })
      // 開始檢測手部與定義回傳處理（onResult）
      hands.onResults(onResults)
      const camera = new Camera(inputVideo.value, {
        onFrame: async () => {
          // 這裡為每幀檢測手部，也加上了drawSign，可以每幀讀取簽名資料並繪圖
          if (store.state.sentLock === true) {
            await hands.send({ image: inputVideo.value })
            drawSign(ctx.value)
            checkHold()
          }
        }
      })
      // 啟動相機
      camera.start()
      console.log('loading complete')
    }

    // overriding hands的onResults
    function onResults (results) {
      width.value = results.image.width
      height.value = results.image.height
      ctx.value.save()
      ctx.value.clearRect(0, 0, results.image.width, results.image.height)
      ctx.value.drawImage(
        results.image,
        0,
        0,
        results.image.width,
        results.image.height
      )
      // 檢測手部
      findHands(results)
      // 畫面卡住解除，載入完成後的執行點，在這邊切換載入畫面和畫布
      if (cameraShow.value === false) {
        loadingShow.value = false
      }
      ctx.value.restore()
    }
    // loadingShow 離開後觸發，將畫布叫回來
    function loadingLeave () {
      cameraShow.value = true
    }
    // 檢測手部，如果有檢測到就繪出骨架
    function findHands (results, draw = false) {
      if (results.multiHandLandmarks.length > 0) {
        detected.value = true
        // 此處移除了迴圈，如果需要檢測雙手，需要改回來
        // landmarks的
        landmarks.prev = landmarks.curr
        landmarks.curr = results.multiHandLandmarks[0]
        drawConnectors(ctx.value, landmarks.curr)
        signProcess(ctx.value, landmarks.curr)
      } else {
        detected.value = false
      }
    }
    // overridding hands的繪圖套件
    function drawConnectors (ctx, landmarks) {
      const COLORLIST = [
        'rgba(255,234,189,0.5)',
        'rgba(128,64,128,0.5)',
        'rgba(255, 206, 8,0.5)',
        'rgba(48,255,48,0.5)',
        'rgba(0,204,255,0.5)'
      ]
      if (landmarks) {
        ctx.save()
        const canvas = ctx.canvas
        ctx.lineWidth = 3
        ctx.lineCap = 'round'
        ctx.lineJoin = 'round'
        for (let i = 1; i <= 17; i = i + 4) {
          ctx.beginPath()
          ctx.strokeStyle = COLORLIST[Math.floor(i / 4)]
          ctx.moveTo(
            landmarks[0].x * canvas.width,
            landmarks[0].y * canvas.height
          )
          ctx.lineTo(
            landmarks[i].x * canvas.width,
            landmarks[i].y * canvas.height
          )
          ctx.lineTo(
            landmarks[i + 1].x * canvas.width,
            landmarks[i + 1].y * canvas.height
          )
          ctx.lineTo(
            landmarks[i + 2].x * canvas.width,
            landmarks[i + 2].y * canvas.height
          )
          ctx.lineTo(
            landmarks[i + 3].x * canvas.width,
            landmarks[i + 3].y * canvas.height
          )
          ctx.stroke()
        }
        for (let i = 0; i <= 20; i++) {
          ctx.save()
          ctx.translate(
            landmarks[i].x * canvas.width,
            landmarks[i].y * canvas.height
          )
          if (i === 0) {
            ctx.rotate((45 * Math.PI) / 180)
          } else if (i % 4 === 1) {
            const angle = Math.atan2(
              landmarks[i].y - landmarks[0].y,
              landmarks[i].x - landmarks[0].x
            )
            const theta = angle * (180 / Math.PI)
            ctx.rotate(((theta - 45) * Math.PI) / 180)
          } else {
            const angle = Math.atan2(
              landmarks[i].y - landmarks[i - 1].y,
              landmarks[i].x - landmarks[i - 1].x
            )
            const theta = angle * (180 / Math.PI)
            ctx.rotate(((theta - 45) * Math.PI) / 180)
          }
          if (i === 0) {
            ctx.fillStyle = 'white'
            ctx.fillRect(-12 / 2, -12 / 2, 12, 12)
            ctx.fillStyle = 'hsl(' + (angleA % 360) + ',100%, 50%)'
            ctx.fillRect(-8 / 2, -8 / 2, 8, 8)
          } else {
            ctx.fillStyle = COLORLIST[Math.floor((i - 1) / 4)]
            ctx.fillRect(-8 / 2, -8 / 2, 8, 8)
          }
          ctx.restore()
        }
        ctx.restore()
      }
    }
    // 監聽靜止狀態，對於靜止狀態的改變，由holdChange接收資料變化
    watch(ifHold, holdChange)
    function holdChange (newValue, oldValue) {
      if (
        newValue === '靜止中' &&
        store.state.handLandmarkPosition.length > 50
      ) {
        holdSecond.value = Date.now()
      } else {
        holdSecond.value = 0
        isHoldOver1Point5Sec.value = false
        signState.value = '開始簽名'
      }
    }
    // 計算fps循環呼叫自己
    function fpsLoop (timestamp) {
      angleA += stepA
      while (times.length > 0 && times[0] <= timestamp - 1000) {
        times.shift()
      }
      times.push(timestamp)
      fps.value = times.length
      // console.log(times.length)
      requestAnimationFrame(fpsLoop)
    }
    requestAnimationFrame(fpsLoop)

    // 元素掛載後傳遞canvas主體給ctx，並初始化
    // 每100毫秒檢測一次手部靜止狀態
    onMounted(() => {
      ctx.value = outputCanvas.value.getContext('2d')
      init()
    })
    // 每100毫秒檢測一下holdSecond的秒數，超過1.5秒就可以加上3秒的靜止動畫
    function checkHold () {
      // if
      if (
        holdSecond.value &&
        Date.now() - holdSecond.value - 1500 > 1500 &&
        store.state.handLandmarkPosition.length > 50
      ) {
        signState.value = '簽名送出'
        if (store.state.sentLock === true) {
          ElNotification({
            title: '簽名已送出！',
            message: '簽名已送出！等待驗證中...',
            type: 'success'
          })
          const body = {
            token: store.state.loginToken,
            landmark: store.state.handLandmarkPosition
          }
          store.dispatch('sentSign', body)
        }
        store.commit('setSentLock', false)
        console.log('3S')
      } else if (holdSecond.value && Date.now() - holdSecond.value > 1500) {
        signState.value = '簽名確認'
        isHoldOver1Point5Sec.value = true
        console.log('1.5S')
      }
    }
    return {
      // mediapipe相關元件
      ctx,
      width,
      height,
      hiddenCamera,
      outputCanvas,
      inputVideo,
      onResults,
      findHands,
      holdSecond,
      // fps
      fps,
      // DOM動畫v-show用
      cameraShow,
      loadingShow,
      loadingLeave,
      // 手部距離
      handDist,
      // 座標檢測資訊
      landmarks,
      // 是否偵測到手，detected:bool，handDetected:DOM，computed，以detected輸出網頁狀態
      handDetected,
      detected,
      // 靜止檢測，在外部js元件useSignCapture定義
      ifHold,
      isHoldOver1Point5Sec,
      // 按鈕icon引入
      Delete,
      // 界面狀態操作
      signState
    }
  }
}
</script>
<style lang="scss" scoped>
:root {
  --hold-progess: 0%;
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
$phones-media: 600px;
.login {
  height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.index-title {
  font-family: consolas;
  font-weight: bold;
  position: absolute;
  color: rgba(255, 255, 255, 0.5);
  transition: 300ms;
  font-size: 25px;
  left: 10px;
  top: 3px;
  &:hover {
    color: rgba(255, 255, 255, 0.85);
    transition: 300ms;
  }
  p {
    font-family: consolas;
    font-size: 12px;
    margin: 0px;
    text-align: left;
  }
}
.powered {
  color: rgba(255, 255, 255, 0.5);
  position: absolute;
  width: 100vw;
  font-size: 12px;
  bottom: 0px;
  margin-bottom: 5px;
}
@media only screen and (max-width: $phones-media) {
  //手機版css
  .login-box {
    font-size: 8vmin;
    color: rgba(255, 255, 255, 0.5);
  }
}
@media only screen and (min-width: $phones-media) {
  //電腦版css
  .loading {
    background-color: rgba(0, 0, 0, 0.25);
    border-radius: 5px;
    color: white;
    font-size: 24px;
    padding: 10px;
  }
  .container {
    height: 100vh;
    background: linear-gradient(
      0deg,
      rgba(54, 153, 203, 0.492) 50%,
      rgba(0, 0, 0, 0) 50%
    );
    background-size: 200% 200%;
    background-position: 0% 0%;
    transition: all 1.5s cubic-bezier(0.33, 1, 0.68, 1);
  }
  .stat {
    mix-blend-mode: hard-light;
    position: absolute;
    bottom: 15px;
    right: 10px;
    font-size: 10vmin;
    writing-mode: vertical-lr;
    font-weight: bold;
    color: rgba(255, 255, 255, 0.35);
  }
  .container.progress {
    background-position: 0% 100%;
  }
  .canvas-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100vw;
    height: 100vh;
  }
  .sign-option {
    text-align: left;
    box-sizing: border-box;
    position: absolute;
    bottom: 0px;
    z-index: 3;
    width: unquote("calc(100% - 20px)");
    padding: 5px;
    margin: 0 10px 10px 10px;
    background-color: rgba(0, 0, 0, 0.5);
  }
  .sig-info {
    width: 235px;
    background-clip: padding-box;
    height: 175px;
    border: rgba(255, 255, 255, 0.5) 7.5px solid;
    background-color: rgb(255, 255, 255);
    position: absolute;
    left: 10px;
    top: 300px;
    border-radius: 5px;
    text-align: center;
    padding: 15px;
  }
  .output-canvas {
    width: 60vw;
    border-radius: 5px;
    border: solid 10px;
    border-color: white;
    vertical-align: bottom;
    filter: drop-shadow(0 0 0.75rem rgba(0, 0, 0, 0.2));
    transform: rotateY(180deg);
  }
  .capture-info {
    width: 250px;
    height: 250px;
    background-color: rgba(255, 255, 255, 0.65);
    position: absolute;
    left: 10px;
    top: 10px;
    border-radius: 5px;
    text-align: left;
    padding: 15px;
  }
  .login-btn {
    width: 100px;
    height: 35px;
    border-radius: 100px;
    background-color: #ffffff;
    border-color: #dcdfe6;
    color: #606266;
    transition: 300ms;
    &:hover {
      color: #606266;
      background-color: #ffffff;
      filter: drop-shadow(2px 2px 2px rgba(0, 0, 0, 0.4));
      border-color: #dcdfe6;
      transition: 300ms;
    }
    &.reg {
      background-color: #8468f3;
      border-color: #dcdfe6;
      color: #ffffff;
      &:hover {
        color: #ffffff;
        filter: drop-shadow(2px 2px 2px rgba(0, 0, 0, 0.4));
        transition: 300ms;
      }
    }
  }
  ::v-deep .el-input__inner {
    border-radius: 100px;
    height: 35px;
    width: 296px;
    margin-top: 10px;
    outline-color: #8468f3;
  }
  .el-input {
    --el-input-focus-border-color: #8f59ce;
  }
}
</style>
