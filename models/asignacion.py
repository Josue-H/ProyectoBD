from providers.database import db

class Asignacion(db.Model):
    id_asignacion = db.Column(db.Integer, primary_key=True)
    id_alumno = db.Column(db.Integer, db.ForeignKey('alumno.id_alumno'), nullable=False)
    id_curso = db.Column(db.Integer, db.ForeignKey('curso.id_curso'), nullable=False)
    id_inscripcion = db.Column(db.Integer, db.ForeignKey('inscripcion.id_inscripcion'), nullable=False)

    alumno = db.relationship('Alumno', back_populates='asignaciones')
    curso = db.relationship('Curso', back_populates='asignaciones_curso')