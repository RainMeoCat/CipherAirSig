// src/composables/useSignCapture.js
import store from '@/store'
import { computed } from 'vue'
export default function useSignCapture (landmarks, detected) {
  const expectedRound = require('expected-round')
  const threshold = 0.3
  let writing = false
  const handPointList = [
    'WRIST',
    'THUMB_CMC',
    'THUMB_MCP',
    'THUMB_IP',
    'THUMB_TIP',
    'INDEX_FINGER_MCP',
    'INDEX_FINGER_PIP',
    'INDEX_FINGER_DIP',
    'INDEX_FINGER_TIP',
    'MIDDLE_FINGER_MCP',
    'MIDDLE_FINGER_PIP',
    'MIDDLE_FINGER_DIP',
    'MIDDLE_FINGER_TIP',
    'RING_FINGER_MCP',
    'RING_FINGER_PIP',
    'RING_FINGER_DIP',
    'RING_FINGER_TIP',
    'PINKY_MCP',
    'PINKY_PIP',
    'PINKY_DIP',
    'PINKY_TIP'
  ]
  function euclidean (p1, p2) {
    const a = p1[0] - p2[0]
    const b = p1[1] - p2[1]
    return Math.sqrt(a * a + b * b)
  }
  // 簽名繪圖
  function drawSign (ctx) {
    // 事先保存畫布資訊
    ctx.save()
    // ctx.filter = 'drop-shadow(0px 0px 2px #fff)'
    // 畫布線條樣式設定
    ctx.lineWidth = 3
    ctx.lineCap = 'round'
    ctx.lineJoin = 'round'
    // 定義線條顏色
    const COLORLIST = {
      index: 'rgba(128,64,128,0.75)',
      middle: 'rgba(255, 206, 8,0.75)',
      ring: 'rgba(48,255,48,0.75)',
      pinky: 'rgba(0,204,255,0.75)'
    }
    // 遍歷抓取筆畫
    for (const index in store.state.signList) {
      // 以這筆畫使用的手勢組合取得筆畫顏色
      ctx.strokeStyle = COLORLIST[store.state.signList[index].pinch]
      // 應對最後一筆筆畫沒有任何筆畫的問題
      if (store.state.signList[index].line.length === 0) {
        break
      }
      // 新路徑
      ctx.beginPath()
      // 首先移動到一條線的第一個點位置以開始畫出一條線
      ctx.moveTo(
        store.state.signList[index].line[0][0],
        store.state.signList[index].line[0][1]
      )
      // 遍歷這條線裡的所有點
      for (let i = 1; i < store.state.signList[index].line.length; i++) {
        // 畫線到此點
        ctx.lineTo(
          store.state.signList[index].line[i][0],
          store.state.signList[index].line[i][1]
        )
      }
      // 建立線條（沒有這個看不到線條）
      ctx.stroke()
      // 筆畫編號的建立工作，首先在網頁上因為webcam的左右鏡相，已經用css修正回來
      // 因此如果直接打字上去，會是左右相反的，因此先把context左右翻轉，打上文字後翻轉回來
      ctx.beginPath()
      ctx.scale(-1, 1)
      ctx.translate(-ctx.canvas.width, 0)
      ctx.fillStyle = COLORLIST[store.state.signList[index].pinch]
      ctx.font = '24pt Gen Jyuu Gothic'
      const textX = store.state.signList[index].line[
        store.state.signList[index].line.length - 1
      ][0]
      const textY = store.state.signList[index].line[
        store.state.signList[index].line.length - 1
      ][1]
      ctx.fillText(
        Math.floor(index) + 1,
        textX - (textX - (ctx.canvas.width / 2)) * 2 + 10,
        textY + 10
      )
      ctx.setTransform(1, 0, 0, 1, 0, 0)
    }
    ctx.restore()
  }

  function signProcess (ctx, landmarks) {
    // 定義此幀之座標點，curr=此幀、prev=上一幀
    const landmarksTemp = []
    for (let i = 0; i < handPointList.length; i++) {
      landmarksTemp.push({
        landmark: handPointList[i],
        x: landmarks[i].x,
        y: landmarks[i].y,
        z: landmarks[i].z
      })
    }
    store.commit('recordPosition', landmarksTemp)
    // 創建距離陣列，這用於取得最小值來判斷提筆
    const distArr = Object.keys(handDist.value).map(function (key) {
      return handDist.value[key]
    })
    for (const index in handDist.value) {
      if (handDist.value[index] < threshold) {
        const X = ctx.canvas.width * landmarks[4].x
        const Y = ctx.canvas.height * landmarks[4].y
        store.commit('pushLinePoint', [X, Y])
        store.commit('setLinePinch', index)
        writing = true
      }
      if (Math.min(...distArr) > threshold && writing === true) {
        // 這裡儲存現在正在第幾條線
        // 斷開線條之後就可以將第幾條線的指標+1，存入簽名列表
        store.commit('indicatorPlus')
        store.commit('newLine')
        writing = false
      }
    }
  }
  // 回傳距離DOM內容，使用curr的座標
  const handDist = computed(() => {
    const CURR = landmarks.curr
    // 先判斷有沒有檢測到手部
    if (detected.value) {
      // 大拇指X,Y,Z
      const X = CURR[4].x
      const Y = CURR[4].y
      const INDEX_X = CURR[8].x
      const INDEX_Y = CURR[8].y
      const MIDDLE_X = CURR[12].x
      const MIDDLE_Y = CURR[12].y
      const RING_X = CURR[16].x
      const RING_Y = CURR[16].y
      const PINKY_X = CURR[20].x
      const PINKY_Y = CURR[20].y
      //  使用整隻手掌的相對距離
      const WRIST_X = CURR[0].x
      const WRIST_Y = CURR[0].y
      const INDEX_MCP_X = CURR[5].x
      const INDEX_MCP_Y = CURR[5].y
      const HAND_SIZE = expectedRound.round10(
        euclidean([WRIST_X, WRIST_Y], [INDEX_MCP_X, INDEX_MCP_Y]),
        -2
      )
      return {
        index: expectedRound.round10(
          euclidean([X, Y], [INDEX_X, INDEX_Y]) / HAND_SIZE,
          -2
        ),
        middle: expectedRound.round10(
          euclidean([X, Y], [MIDDLE_X, MIDDLE_Y]) / HAND_SIZE,
          -2
        ),
        ring: expectedRound.round10(
          euclidean([X, Y], [RING_X, RING_Y]) / HAND_SIZE,
          -2
        ),
        pinky: expectedRound.round10(
          euclidean([X, Y], [PINKY_X, PINKY_Y]) / HAND_SIZE,
          -2
        )
      }
    } else {
      return {
        index: '未偵測',
        middle: '未偵測',
        ring: '未偵測',
        pinky: '未偵測'
      }
    }
  })
  // 靜止檢測，使用兩個座標點之間的差來判斷手部靜止
  const ifHold = computed(() => {
    const CURR = landmarks.curr
    const PREV = landmarks.prev
    if (!detected.value) {
      return '未偵測到手部'
    } else if (!PREV.length > 0) {
      return '運動中'
    } else {
      for (let i = 0; i < CURR.length; i++) {
        if (Math.abs(CURR[i].x - PREV[i].x) > 0.008) {
          return '運動中'
        }
        if (Math.abs(CURR[i].y - PREV[i].y) > 0.008) {
          return '運動中'
        }
      }
    }
    return '靜止中'
  })

  return {
    drawSign,
    euclidean,
    handDist,
    ifHold,
    signProcess
  }
}
