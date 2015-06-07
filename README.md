```
  wget https://bootstrap.pypa.io/get-pip.py
  sudo python3 get-pip.py
  sudo pip install Django
  sudo apt-get install libmysqlclient-dev
  sudo pip install mysqlclient
```
  
Зайти в /etc/mysql/my.cnf  
Дописать:
```
  [client]
  ...
  default-character-set=utf8
  ...
  [mysqld]
  ...
  character-set-server=utf8
  collation-server=utf8_general_ci
```

```
  mysql -u root -p #в баше

  CREATE USER 'blog_user'@'localhost' IDENTIFIED BY 'tralala';
  CREATE DATABASE blog;
  GRANT ALL PRIVILEGES ON blog . * TO 'blog_user'@'localhost';
  FLUSH PRIVILEGES;
```

```
  wget http://getbootstrap.com/2.3.2/getting-started.html/assets/bootstrap.zip
  ...
