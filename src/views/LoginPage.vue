<template>
  <div style="position:absolute;z-index:1;width:100vw;height:100vh;top:0px;left:0px">
    <div class="login">
      <div class="login-box">
        <div style="margin-bottom: 10px">
          登入
        </div>
        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="rules"
          status-icon
          hide-required-asterisk
        >
          <el-form-item
            label="帳號"
            prop="username"
          >
            <el-input
              v-model="loginForm.username"
              autocomplete="off"
              placeholder="輸入帳號"
            />
          </el-form-item>
          <el-form-item
            label="密碼"
            prop="password"
          >
            <el-input
              v-model="loginForm.password"
              type="password"
              autocomplete="off"
              placeholder="輸入密碼"
            />
          </el-form-item>
          <el-form-item style="display: inline-block">
            <el-button
              type="primary"
              class="login-btn"
              @click="changePage('')"
            >
              登入
            </el-button>
            <!-- <el-button
              class="login-btn reg"
              @click="resetForm()"
            >
              註冊
            </el-button> -->
          </el-form-item>
        </el-form>
      </div>
      <div class="powered">
        Powered by <img
          src="@/assets/MPlogo.png"
          style="width:16px;filter: grayscale(100%) brightness(100) opacity(0.5);vertical-align:text-top"
        >Mediapipe.
      </div>
    </div>
  </div>
</template>
<script>
import { reactive, ref } from 'vue'
import { useStore } from 'vuex'
export default {
  name: 'LoginPage',
  setup () {
    const loginFormRef = ref(null)
    const rules = {
      username: [{ required: true, message: '請輸入帳號!', trigger: 'change' }],
      password: [{ required: true, message: '請輸入密碼!', trigger: 'change' }]
    }
    const loginForm = reactive({
      username: 'F110156111@nkust.edu.tw',
      password: 'test'
    })
    const store = useStore()
    function setSha () {
      const sha256 = require('js-sha256').sha256// 這裡用的是require方法，所以沒用import
      return sha256(loginForm.password)// 要加密的密碼
    }
    function changePage (page) {
      loginFormRef.value.validate(valid => {
        if (valid) {
          const body = {
            account: loginForm.username,
            password: setSha()
          }
          store.dispatch('loginAndGetToken', body)
        }
      })
    }
    return {
      changePage,
      loginForm,
      loginFormRef,
      rules
    }
  }
}
</script>
<style lang="scss" scoped>
$phones-media: 600px;
.login {
  height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow:hidden
}
.index-title{
  font-family: consolas;
  font-weight: bold;
  position: absolute;
  color:rgba(255,255,255, 0.5);
  transition: 300ms;
  font-size: 25px;
  left:10px;
  top: 3px;
  &:hover {
      color:rgba(255, 255, 255, 0.85);
      transition: 300ms;
  }
  p {
    font-family: consolas;
    font-size:12px;
    margin:0px;
    text-align:left;
  }
}
.powered{
  color:rgba(255,255,255, 0.5);
  position: absolute;
  width:100vw;
  font-size: 12px;
  bottom: 0px;
  margin-bottom: 5px;
}
@media only screen and (max-width: $phones-media) {
  //手機版css
  .login-box{
    font-size: 8vmin;
    color:rgba(255,255,255, 0.5)
  }
}
@media only screen and (min-width: $phones-media) {
  //電腦版css
    .login-box{
    font-size: 3.5vmin;
    color:rgba(0, 0, 0, 0.5);
    width: 295px;
    padding:25px 20px;
    background-color: rgba(255,255,255,0.45);
    border-radius: 5px;
  }
  .forget-pwd {
    color:rgba(255,255,255, 0.5)!important;
    transition: 300ms;
    &:hover {
      color:rgb(0, 195, 255)!important;
      transition: 300ms;
    }
  }
  .login-btn{
    width: 100px;
    height: 35px;
    border-radius:100px;
    background-color: #ffffff;
    border-color: #dcdfe6;
    color:#606266;
    transition: 300ms;
    &:hover {
      color:#606266;
      background-color: #ffffff;
      filter: drop-shadow(2px 2px 2px rgba(0, 0, 0, 0.4));
      border-color: #dcdfe6;
      transition: 300ms;
    }
    &.reg{
      background-color:#8468F3;
      border-color: #dcdfe6;
      color:#ffffff;
      &:hover {
        color:#ffffff;
        filter: drop-shadow(2px 2px 2px rgba(0, 0, 0, 0.4));
        transition: 300ms;
      }
    }
  }
  ::v-deep .el-form-item__label{
    color:rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
  }
  .el-input{
    --el-input-focus-border-color: #8f59ce;
  }
}

</style>
