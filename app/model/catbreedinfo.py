from app import db

class CatBreedInfo(db.Model):
    __tablename__ = 'cat_breed_info'

    id = db.Column(db.Integer, primary_key=True)
    breed_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<CatBreedInfo {self.breed_name}>"