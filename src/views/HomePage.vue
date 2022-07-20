<template>
  <div class="HomePage">
    <div>
      <img
        alt="Vue logo"
        src="https://imgur.com/Ij8S4gq.png"
      >
      <br>
      <div class="pray">
        - 祝demo成功 -
      </div>
    </div>
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
<style scoped>
  .HomePage{
    display:flex;
    justify-content: center;
    align-items: center;
    width:100vw;
    height:100vh
  }
  .pray {
    mix-blend-mode: color-burn;
    color: rgba(50, 50, 50, 0.3);
    font-size:26px;
    font-weight:bold
  }
</style>
