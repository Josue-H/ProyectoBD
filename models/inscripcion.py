from providers.database import db

class Inscripcion(db.Model):
    id_inscripcion = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    id_alumno = db.Column(db.Integer, db.ForeignKey('alumno.id_alumno'), nullable=False)
    id_encargado = db.Column(db.Integer, db.ForeignKey('encargado.id_encargado'), nullable=False)
    id_pago = db.Column(db.Integer, db.ForeignKey('pago.id_pago'), nullable=False)

    # se utiliza un backref o un backpopulates para definir las relaciones entre los modelos
    # relaciones
    alumno = db.relationship('Alumno', backref='inscripciones')
    encargado = db.relationship('Encargado', backref='inscripciones')
    pago = db.relationship('Pago', backref='inscripciones')
