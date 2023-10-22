from providers.database import db
class Profesor(db.Model):
    id_profesor = db.Column(db.Integer, primary_key=True, autoincrement=False)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    profesion = db.Column(db.String(60))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)

    usuario = db.relationship('Usuario', backref='profesores')
    asignaciones = db.relationship('AsignacionCur', back_populates='profesor')
