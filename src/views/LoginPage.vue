<template>
  <div class="login">
    <div class="login-box">
      登入
    </div>
  </div>
</template>
<style lang="scss" scoped>
$phones-media: 600px;
.login {
  background: linear-gradient(#7361E4, #F8ADFE);
  height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;

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
    color:rgba(255,255,255, 0.5)
  }
  }

</style>
