from providers.database import db

class Alumno(db.Model):
    id_alumno = db.Column(db.Integer, primary_key=True, autoincrement=False)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    genero = db.Column(db.String(10))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
   
    usuario = db.relationship('Usuario', backref='alumnos')

    notas = db.relationship('Nota', back_populates='alumno')
    asignaciones = db.relationship('Asignacion', back_populates='alumno')


