# Jetson NX setup

# Images
> https://developer.nvidia.com/embedded/learn/get-started-jetson-xavier-nx-devkit

> https://developer.nvidia.com/embedded/jetpack-archive

# 啟動設定
```=bash

sudo apt-get install python3-pip
sudo pip3 install jetson-stats

sudo modprobe spidev
```

# 主程式

你沒看錯這裡只有一支embedded\rpi_main.py
主要目的是擷取溫度資料回傳到資料庫中，後端API會將其轉換為BASE64方式儲存
以便瀏覽器讀取BASE64圖片(BASE64是可以用來傳圖片的)
這是一個取巧的寫法，但前端很方便實作