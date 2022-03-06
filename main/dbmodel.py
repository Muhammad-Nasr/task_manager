from main import db, bcrypt, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from flask import current_app



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.Integer, nullable=False)
    profile_image = db.Column(db.String, nullable=False, default='default.jpg')
    task = db.relationship('Tasks', backref='user_task', lazy=True)

    @property
    def password_hash(self):
        return self.password_hash

    @password_hash.setter
    def password_hash(self, input_password):
        self.password = bcrypt.generate_password_hash(input_password).decode('utf-8')

    def check_correct_password(self, attempted_password):
        return bcrypt.check_password_hash(pw_hash=self.password, password= attempted_password)

## token

    def send_user_token(self, expire_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expire_sec )
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_user_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            user_id = s.loads(token)['user_id']

        except:
            return None

        return User.query.get(user_id)


class Tasks(db.Model):
    __tablename__ = "tasks"
    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey ('users.id'))

    def __repr__(self):
        return f"Task {self.name}"

