from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # Эта строчка нужна, чтобы подключиться к базе данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # отключает сигнализацию об изменении объектов внутри базы данных

db: SQLAlchemy = SQLAlchemy(app) # Создание объекта, через который будем работать с базой данных

class User(db.Model):  # В скобках модель, чтобы в дальнейшем создать именно базу данных
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # В скобках описываем поля таблицы

    def __repr__(self):  # метод определяет, как объект модели будет выглядеть в виде строки
        return f'<User {self.username}>'

with app.app_context(): # Функция создаёт контекст приложения, нужен для работы с базой данных
    db.create_all() # Создание всей таблицы, которые определены в классе User

@app.route('/add_user')  # С помощью декоратора создаём маршрут, который будет вызывать функцию
def add_user():  # Функция будет создавать объект класса User
    new_user = User(username='new_username')
    try:
        db.session.add(new_user)  # Добавляем в сессию
        db.session.commit()  # Сохраняем изменения в базу данных
        return 'User added'  # Вывод сообщения о том, что юзер добавлен в базу данных
    except Exception as e:
        db.session.rollback()
        return f'Error: {str(e)}'

@app.route('/users')
def get_users():
    users = User.query.all() # Получаем всех юзеров из базы данных и сохраняем в переменную users
    return str(users)

if __name__ == '__main__':
    app.run(debug=True)