from flaskserver import db

class ClickstreamLink(db.Model):
    __tablename__ = "hierarchy_links"

    id = db.Column(db.Integer, primary_key=True)
    link_from = db.Column(db.Integer, db.ForeignKey("articles.id"), nullable=False)
    link_to = db.Column(db.Integer, db.ForeignKey("articles.id"), nullable=False)
    num_refs = db.Column(db.Integer)

    def __init__(self, link_from, link_to, num_refs):
        self.link_from = link_from
        self.link_to = link_to
        self.num_refs = num_refs

    def __repr__(self):
        return "<ClickstreamLink {} {} {}>".format(
                self.link_from,
                self.link_to,
                self.num_refs)

    def to_dict(self):
        return {
            'id', self.id,                  \
            'link_from', self.link_from,    \
            'link_to', self.link_to,        \
            'num_refs', self.num_refs                
        }
