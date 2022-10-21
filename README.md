# [CipherAirSig](https://projects.rainmeocat.com/)
CipherAirSig可以從視覺上捕捉使用者的手部骨架，並應用手勢變化來簽名，本系統規劃了四種手勢， 四種手勢對應每一個筆畫，依據筆畫順序能產生出一個編碼序列，作為密碼，能夠增加簽名生物認證的安全性，同時也會以筆跡、簽名速度來進行驗證。

![](https://i.imgur.com/RVgvTj4.png)

系統尚在構建中，尚不開放註冊，僅提供預設的兩組簽名/兩組帳號供測試，目前只能在電腦上使用，請使用Chrome/edge瀏覽器，並開啟網頁的攝像頭權限。
## 前端
### 專案依賴安裝
```
npm install
```

### 開發
```
npm run serve
```

### 打包
```
npm run build
```

### Lint和自動修正
```
npm run lint
```
### API URL
```
frontend/src/store/index.js:
13: url: 'https://projects.rainmeocat.com/api/',
```
## 後端
### 依賴安裝
```
pip3 install -r requirements.txt
```
### API URL
```
backend/app/config.py:
8: API_BASIC_URL = "https://projects.rainmeocat.com/api"
```

## 環境
> 部屬環境ubuntu 20.04 in AWS EC2
### nginx
> 記得在EC2開放port 80、443

```
sudo apt isntall nginx
sudo apt install certbot
sudo apt install python3-certbot-nginx
sudo certbot --nginx -d YOUR.DOMAIN.NAME 

```
`/etc/nginx/sites-available/default`
1. root指向打包位置
1. [處理vue-router以history產生的重新指令404問題](https://juejin.cn/post/7140073647427256350)
### Database
#### marialdb install
> 安裝完請記得在EC2把port 3306打開

```=bash
sudo apt install mariadb-server

sudo mysql_secure_installation
#all agree

sudo mysql

CREATE USER 'USERNAME'@'%' IDENTIFIED BY 'PASSWORD';
CREATE DATABASE BAS default character set utf8mb4 collate utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON BAS.* TO 'USERNAME'@'%';

sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
bind=0.0.0.0

sudo systemctl restart mysql
```
