<template>
  <div style="position:absolute;z-index:1;">
    <div class="HomePage">
      <div>
        <iframe
          style="width:45vw;height:53vh;border-radius:10px;filter:drop-shadow(2px 2px 3px rgba(0,0,0,0.5));"
          src="https://www.youtube-nocookie.com/embed/NbQSbZvmfG0?controls=0&rel=0"
          title="YouTube video player"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
        />
        <br>
        <div class="pray">
          - 目前不開放註冊，開放兩組帳號和簽名測試 -
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'HomePage',
  components: {}
}
</script>
<style scoped>
.HomePage {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100vw;
  height: 100vh;
  z-index: 1;
}
.pray {
  color: rgba(212, 92, 0, 0.484);
  font-size: 20px;
}
</style>
