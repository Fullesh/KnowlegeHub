<h1>Сервис KnowlegeHub.</h1>

<h3>Сервис "Образовательные модули" необходим для удобного поиска образовательных модулей. Каждый модуль содержит в себе набор уроков связанных с данным модулем. \
<h3>Реализация произведена фреймворками Django-REST-Framework и Django. Документация реализована при помощи DRF-YASG</h3>


## Запуск проекта с использованием Docker

### Шаги по запуску

1. **Клонируйте репозиторий**
    ```bash
    git clone https://github.com/Fullesh/KnowlegeHub.git
    cd KnowlegeHub
    ```

2. **Переименуйте пример файла окружения с .env_example в .env и отредактируйте его**



4. **Постройте и запустите контейнеры Docker**
    ```
    docker-compose up --build
    ```

5. **Создание суперпользователя**
   ```
   docker-compose exec app python manage.py csu
   ```
   
    *Дополнительно* \
    Данные для входа под аккаунтом администратора: \
    *Логин: admin@service.py* \
    *Пароль: 1* 

### Доступ к приложению
- Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000)
- Админ панель Django: [http://localhost:8000/admin](http://localhost:8000/admin)

### Остановка контейнеров
Для остановки контейнеров используйте следующую команду:

```
docker-compose down
```

