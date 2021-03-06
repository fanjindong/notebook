from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        # 告诉 Python 如何打印这个类的对象。我们将用它来调试
        return '<User %r>' % (self.nickname)
