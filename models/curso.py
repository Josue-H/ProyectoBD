from providers.database import db

class Curso(db.Model):
    id_curso = db.Column(db.Integer, primary_key=True, autoincrement=False)
    descripcion = db.Column(db.String(50))
    id_grado = db.Column(db.Integer, db.ForeignKey('grado.id_grado'), nullable=False)
 


    #relaciones
    grado = db.relationship('Grado', backref='cursos')
    nota = db.relationship('Nota', back_populates='curso_nota', lazy=True)

    asignaciones_curso = db.relationship('Asignacion', back_populates='curso')