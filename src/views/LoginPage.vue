<template>
  <div style="position:absolute;z-index:1;width:100vw;height:100vh;top:0px;left:0px">
    <div class="login">
      <div class="login-box">
        登入
        <el-input
          v-model="input"
          placeholder="輸入帳號/電子信箱"
        />
        <el-input
          v-model="input"
          placeholder="輸入密碼"
        />
        <el-link
          :underline="false"
          class="forget-pwd"
        >
          忘記密碼
        </el-link>
        <div style="margin-top:10px">
          <el-button
            round
            size="large"
            class="login-btn"
          >
            登入
          </el-button>
          <el-button
            round
            size="large"
            class="login-btn reg"
          >
            註冊
          </el-button>
        </div>
      </div>
      <div class="powered">
        Powered by CipherSign, <img
          src="@/assets/MPlogo.png"
          style="width:16px;filter: grayscale(100%) brightness(100) opacity(0.5);vertical-align:text-top"
        >Mediapipe.
      </div>
      <div class="index-title">
        CipherSignDemo.com<br>
        <p>Trusted cipher in-air signaturesystem</p>
      </div>
    </div>
  </div>
</template>
<script>
import { ref } from 'vue'

export default {
  name: 'LoginPage',
  setup () {
    const input = ref('')
    return {
      input
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
    color:rgba(255,255,255, 0.5);
    width: 295px;
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
  ::v-deep .el-input__inner{
    border-radius:100px;
    height: 35px;
    width: 296px;
    margin-top:10px;
    outline-color: #8468F3;
  }
  .el-input{
    --el-input-focus-border-color: #8f59ce;
  }
}

</style>
