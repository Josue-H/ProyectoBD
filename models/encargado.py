from providers.database import db

class Encargado(db.Model):
    id_encargado = db.Column(db.Integer, primary_key=True, autoincrement=False)
    nombre = db.Column(db.String(50))
    telefono = db.Column(db.String(10))
    direccion = db.Column(db.String(50))
    correo = db.Column(db.String(50))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    usuario = db.relationship('Usuario', backref='encargados')
