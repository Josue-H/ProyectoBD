from providers.database import db

class AsignacionCur(db.Model):
    id_profesor = db.Column(db.Integer, db.ForeignKey('profesor.id_profesor'), primary_key=True)
    id_curso = db.Column(db.Integer, db.ForeignKey('curso.id_curso'), primary_key=True)
    seccion = db.Column(db.String(3))

    # Definir la relación con el curso
    curso = db.relationship('Curso', backref='asignaciones')  
   # Definir la relación con el profesor
    profesor = db.relationship('Profesor', back_populates='asignaciones')

