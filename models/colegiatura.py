from providers.database import db

class Colegiatura(db.Model):
    id_colegiatura = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.String(10))
    id_alumno = db.Column(db.Integer, db.ForeignKey('alumno.id_alumno'), nullable=False)
    id_pago = db.Column(db.Integer, db.ForeignKey('pago.id_pago'), nullable=False)
    id_inscripcion = db.Column(db.Integer, db.ForeignKey('inscripcion.id_inscripcion'), nullable=False) 
    alumno = db.relationship('Alumno', backref='colegiaturas')
    pago = db.relationship('Pago', backref='colegiaturas')
