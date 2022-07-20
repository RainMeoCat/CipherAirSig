<template>
  <div class="HomePage">
    <el-row class="user-info">
      <el-col
        :span="10"
        style="display:flex;justify-content: center;align-items: center;"
      >
        <el-image
          style="width: 60%; height: 60%; border-radius:50%"
          :src="$store.state.userInfo.avatar"
          fit="cover"
        />
      </el-col>
      <el-col :span="14">
        <div>
          帳號: {{ $store.state.userInfo.account }} <br>
          信箱: {{ $store.state.userInfo.email }} <br>
          最後一次登入: {{ $store.state.userInfo.last_login }} <br>
          註冊時間: {{ $store.state.userInfo.register_time }} <br>
          名字: {{ $store.state.userInfo.user_name }}
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'HomePage',
  components: {
  }
}
</script>
<style>
  .HomePage{
    display:flex;
    justify-content: center;
    align-items: center;
    width:100vw;
    height:100vh
  }
  .user-info{
    display:flex;
    text-align: left;
    align-items: center;
    background-color: rgba(255,255,255,0.5);
    width:50vw;
    height: 40vh;
    font-size: 18px;
    line-height: 54px;
    border-radius: 10px
  }
  .pray {
    font-size:26px;
    color:rgba(255,255,255,0.5);
    font-weight:bold
  }
</style>
