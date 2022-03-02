<template>
  <div style="  background: linear-gradient(#7361E4, #F8ADFE);height: 100vh;width: 100vw;">
    <ul class="circles">
      <li
        v-for="n in 10"
        :key="n"
      />
    </ul>
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
