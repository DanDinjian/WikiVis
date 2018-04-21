from flaskserver import db

class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Article {}>".format(self.name)

    def to_dict(self):
        return {
            'id': self.id,      \
            'name': self.name   \
        }

