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
<style>
  .HomePage{
    display:flex;
    justify-content: center;
    align-items: center;
    width:100vw;
    height:100vh
  }
  .pray {
    font-size:26px;
    color:rgba(255,255,255,0.5);
    font-weight:bold
  }
</style>
