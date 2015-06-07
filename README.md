Для начала установим все для django:
```
  sudo python3 get-pip.py
  sudo pip install Django
  sudo apt-get install libmysqlclient-dev
  sudo pip install mysqlclient
```

После первой лабоартоной установлена mysql, немножко переконфигурируем, чтобы можно было писать в utf-8
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

Еще надо создать в mysql базу данных для проекта django:
```
  mysql -u root -p #в баше

  CREATE USER 'blog_user'@'localhost' IDENTIFIED BY 'tralala';
  CREATE DATABASE blog;
  GRANT ALL PRIVILEGES ON blog . * TO 'blog_user'@'localhost';
  FLUSH PRIVILEGES;
```

Запускаем:
```
  ./manage.py runserver
```

Открываем браузер заходим на localhost:8000 и можем потыкать что нить. (Посты можно создать в localhost:8000/profile, остальное кажется очевидно)
