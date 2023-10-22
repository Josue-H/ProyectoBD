from providers.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from models.rol import Rol
from models.asignacion_rol import AsignacionRol

class Usuario(db.Model, UserMixin):
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=False)
    usuario = db.Column(db.String(60), unique=True, nullable=False)
    contraseña = db.Column(db.String(128), nullable=False)
    
    # Relaciones
    asignacion_rol = db.relationship('AsignacionRol', back_populates='usuario', lazy=True)
    administradores = db.relationship('Administrador', back_populates='usuario', lazy=True)

 
    def __repr__(self):
        return '<Usuario {}>'.format(self.usuario)

    def set_password(self, password):
        # Genera un hash de la contraseña y la almacena en la base de datos
        self.contraseña = generate_password_hash(password)

    def check_password(self, password):
        # Verifica si la contraseña proporcionada coincide con el hash almacenado
        return check_password_hash(self.contraseña, password)

    def get_id(self):
        return str(self.id_usuario)  # Convierte el ID a cadena

    def get_rol(self):
        if self.asignacion_rol:
            for asignacion in self.asignacion_rol:
                rol_id = asignacion.id_rol
                rol = Rol.query.filter_by(id_rol=rol_id).first()
                if rol:
                    return rol.descripcion

        return 'sin_rol'
    
    def is_admin(self):
        return self.get_rol == 'administrador'
    
    def is_student(self):
        return self.get_rol == 'alumno'
    
    def is_teacher(self):
        return self.get_rol == 'profesor'
    
    def is_encargado(self):
        return self.get_rol == 'encargado'
