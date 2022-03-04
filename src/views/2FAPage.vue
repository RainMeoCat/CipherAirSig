<template>
  <div class="container">
    <video
      ref="inputVideo2"
      style="display:none;width:70vw;height:60vh"
    />
    <canvas
      ref="outputCanvas"
      class="outputCanvas"
      style="width:70vw"
      :width="width"
      :height="height"
    />
  </div>
</template>
<script>
import { ref, computed, onMounted } from 'vue'
import { Hands, HAND_CONNECTIONS, VERSION } from '@mediapipe/hands'
import { Camera } from '@mediapipe/camera_utils'
import { drawConnectors, drawLandmarks } from '@mediapipe/drawing_utils'
export default {
  name: 'LoginPage',
  setup () {
    const input = ref('')
    const number = ref(null)
    const ctx = ref(null)
    const width = ref(null)
    const height = ref(null)
    const inputVideo2 = ref(null)
    const outputCanvas = ref(null)

    const inputVideo = computed(() => {
      return inputVideo2.value
    })

    function init () {
      console.log('loading...')
      const hands = new Hands({
        locateFile: (file) => {
          return `https://cdn.jsdelivr.net/npm/@mediapipe/hands@${VERSION}/${file}`
        }
      })

      hands.setOptions({
        modelComplexity: 1,
        maxNumHands: 1,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5
      })
      hands.onResults(onResults)
      const camera = new Camera(inputVideo.value, {
        onFrame: async () => {
          await hands.send({ image: inputVideo.value })
        }
      })
      camera.start()
      console.log('loading complete')
    }

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
      findHands(results)
      ctx.value.restore()
    }

    function findHands (results, draw = true) {
      if (results.multiHandLandmarks.length > 0) {
        for (const landmarks of results.multiHandLandmarks) {
          drawConnectors(ctx.value, landmarks, HAND_CONNECTIONS, {
            color: '#00FF00',
            lineWidth: 5
          })
          if (draw) {
            drawLandmarks(ctx.value, landmarks, {
              color: '#FF0000',
              lineWidth: 2
            })
          }
        }
      }
    }

    onMounted(() => {
      ctx.value = outputCanvas.value.getContext('2d')
      init()
    })

    return {
      input,
      number,
      ctx,
      width,
      height,
      inputVideo2,
      outputCanvas,
      inputVideo,
      onResults,
      findHands
    }
  }
}

</script>
<style lang="scss" scoped>
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
  .login-box {
    font-size: 3.5vmin;
    color: rgba(255, 255, 255, 0.5);
    width: 295px;
  }
  .forget-pwd {
    color: rgba(255, 255, 255, 0.5) !important;
    transition: 300ms;
    &:hover {
      color: rgb(0, 195, 255) !important;
      transition: 300ms;
    }
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
