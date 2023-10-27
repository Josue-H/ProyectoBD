from providers.database import db
class Administrador(db.Model):
    id_administrador = db.Column(db.Integer, primary_key=True, autoincrement=False)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)

    usuario = db.relationship('Usuario', back_populates='administradores')
 