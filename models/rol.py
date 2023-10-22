from providers.database import db

class Rol(db.Model):
    id_rol = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(20), nullable=False)
    
    # Relación con AsignacionRol
    asignaciones = db.relationship('AsignacionRol', back_populates='rol', lazy=True)

 