import { createStore } from 'vuex'
import 'element-plus/theme-chalk/src/message.scss'
import 'element-plus/theme-chalk/src/index.scss'
import { ElNotification } from 'element-plus'
import router from '../router'
import axios from 'axios'
export default createStore({
  state: {
    signList: [{
      line: [],
      pinch: ''
    }],
    url: 'http://127.0.0.1:5000/api/',
    handLandmarkPosition: [],
    strokeIndicator: 0,
    signMode: '',
    loginToken: '',
    crToken: '',
    twoFAToken: '',
    sentLock: true,
    sigPic: require('@/assets/Sig1.png'),
    userInfo: {
      account: '',
      email: '',
      last_login: '',
      register_time: '',
      user_name: '',
      avatar: ''
    }
  },
  getters: {
    returnModeColor (state) {
      return {
        gesture: state.signMode === 'gesture'
      }
    }
  },
  mutations: {
    indicatorPlus (state) {
      state.strokeIndicator++
    },
    pushLinePoint (state, point) {
      state.signList[state.strokeIndicator].line.push(point)
    },
    setLinePinch (state, pinch) {
      state.signList[state.strokeIndicator].pinch = pinch
    },
    setSigPic (state, num) {
      state.sigPic = require('@/assets/Sig' + num + '.png')
    },
    recordPosition (state, landmarks) {
      state.handLandmarkPosition.push(
        {
          unix_time: Date.now(),
          frame_sequence: state.handLandmarkPosition.length + 1,
          landmark: landmarks
        })
    },
    newLine (state) {
      state.signList.push({
        line: [],
        pinch: ''
      })
    },
    resetSign (state) {
      state.signList = [{
        line: [],
        pinch: ''
      }]
      state.handLandmarkPosition = []
      state.strokeIndicator = 0
      state.sentLock = true
    },
    changeMode (state, mode) {
      state.signMode = mode
    },
    setToken (state, token) {
      state.loginToken = token
    },
    set2FAToken (state, token) {
      state.twoFAToken = token
    },
    setSentLock (state, LockStat) {
      state.sentLock = LockStat
    },
    setUserInfo (state, info) {
      state.userInfo = info
    },
    setCR (state, cr) {
      state.crSymbol = cr
    },
    setCRToken (state, token) {
      state.crToken = token
    }
  },
  actions: {
    loginAndGetToken (context, body) {
      axios.post(context.state.url + 'user/login', body)
        .then((response) => {
          console.log(response)
          context.commit('setToken', response.data.token)
          router.push('/2fa')
        })
        .catch((error) => {
          console.log(error)
          ElNotification({
            title: '錯誤',
            message: '帳號或密碼錯誤。',
            type: 'error'
          })
        })
    },
    sentSign (context, body) {
      let url = ''
      url = context.state.url + 'gsign/2fa'
      axios.post(url, body)
        .then((response) => {
          ElNotification({
            title: '簽名通過！',
            message: '簽名通過！',
            type: 'success'
          })
          context.commit('set2FAToken', response.data.token)
          context.dispatch('getUserInfo')
          context.commit('resetSign')
          router.push('/user')
        })
        .catch((error) => {
          console.log(error)
          ElNotification({
            title: '錯誤',
            message: '簽名遭到拒絕！',
            type: 'error'
          })
          context.commit('setSentLock', true)
          context.commit('resetSign')
        })
    },
    getUserInfo (context) {
      axios.post(context.state.url + 'user/info', { token: context.state.twoFAToken })
        .then((response) => {
          context.commit('setUserInfo', response.data)
        })
        .catch((error) => {
          console.log(error)
        })
    }
  },
  modules: {
  }
})
