from providers.database import db
class Nota(db.Model):
    id_alumno = db.Column(db.Integer, db.ForeignKey('alumno.id_alumno'), primary_key=True)
    id_curso = db.Column(db.Integer, db.ForeignKey('curso.id_curso'), primary_key=True)
    nota = db.Column(db.Integer)

    # Corregir las relaciones con Alumno y Curso
    alumno = db.relationship('Alumno', back_populates='notas')
    curso_nota = db.relationship('Curso', back_populates='nota')
