from providers.database import db
class Grado(db.Model):
    id_grado = db.Column(db.Integer, primary_key=True, autoincrement=False)
    descripcion = db.Column(db.String(35))
