from providers.database import db

class AsignacionRol(db.Model):
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), primary_key=True)
    id_rol = db.Column(db.Integer, db.ForeignKey('rol.id_rol'), primary_key=True)

    # Relación con Usuario
    usuario = db.relationship('Usuario', back_populates='asignacion_rol')
    
    # Relación con Rol
    rol = db.relationship('Rol', back_populates='asignaciones')

