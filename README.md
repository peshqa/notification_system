# Система уведомлений Django

## Требования
- Python 3.8+
- Django 4.0+
- Channels 3.0+
- Redis (для production)

## Установка
1. Клонировать репозиторий:
   ```
   git clone https://github.com/peshqa/notification_system.git
   cd notification_system
   ```
2. Установить зависимости:
   ```
   pip install -r requirements.txt
   ```
3. Применить миграции:
   ```
   python manage.py migrate
   ```
4. Загрузить тестовые данные:
   ```
   python manage.py create_test_data
   ```
5. Запустить сервер:
   ```
   python manage.py runserver
   ```
6. Запустить сервер:
   ```
   python manage.py runserver
   ```
## Тестирование
1. Войти в админ-панель (/admin) как:

 - Суперпользователь: admin/adminpass
 
 - Обычный пользователь: user1/userpass

2. Проверить:

 - Обычные пользователи видят только свои записи

 - Суперпользователь видит все записи

 - Фильтры работают по владельцу и дате создания

 - При изменении записи появляется уведомление

 - При смене владельца уведомления получают оба пользователя

 - Уведомления автоматически исчезают через 5 секунд