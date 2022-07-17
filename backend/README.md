# AIRSIGN BAS BACKEND
## environment
### nginx
```
sudo apt isntall nginx
sudo apt install certbot
sudo apt install python3-certbot-nginx
sudo certbot --nginx -d bas.shiya.site

```
### Database
#### marialdb install


```=bash
sudo apt install mariadb-server

sudo mysql_secure_installation
#all agree

sudo mysql

CREATE USER 'italab'@'%' IDENTIFIED BY 'ma308';
CREATE DATABASE BAS default character set utf8mb4 collate utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON BAS.* TO 'italab'@'%';

sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
bind=0.0.0.0

sudo systemctl restart mysql
```

