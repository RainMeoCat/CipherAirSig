# AIRSIGN BAS BACKEND
## environment
### Database
#### marialdb install


```=bash
sudo apt install mariadb-server

sudo mysql_secure_installation

sudo mysql

CREATE USER 'italab'@'%' IDENTIFIED BY 'ma308';
CREATE DATABASE bas default character set utf8mb4 collate utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON bas.* TO 'italab'@'%';

sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
bind=0.0.0.0

sudo systemctl restart mysql
```

