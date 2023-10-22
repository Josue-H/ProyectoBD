#decorators.py
from functools import wraps #decoradores
from flask import abort, current_app, request # gestión de peticiones al servidor
from flask_login import current_user #gestión de inicios de sesión y permisos 
# from models import usuario

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # Verificar si el usuario actual es un administrador
        if not current_user.is_authenticated or current_user.get_rol() != 'administrador':
            current_app.logger.info(f"Acceso prohibido para la ruta {request.path}")
            abort(403)  # Acceso prohibido si no es un administrador
        return func(*args, **kwargs)
    return decorated_view

def teacher_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # Verificar si el usuario actual es un profesor
        if not current_user.is_authenticated or  current_user.get_rol() != 'profesor':
            current_app.logger.info(f"Acceso prohibido a la ruta {request.path}")
            abort(403)  # Acceso prohibido si no es un profesor
        return func(*args, **kwargs)
    return decorated_view

def student_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # Verificar si el usuario actual es un alumno
        if not current_user.is_authenticated or  current_user.get_rol() != 'alumno':
            current_app.logger.info(f"Acceso prohibido a la ruta {request.path}")
            abort(403)  # Acceso prohibido si no es un alumno
        return func(*args, **kwargs)
    return decorated_view


def encargado_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # Verificar si el usuario actual es un alumno
        if not current_user.is_authenticated or  current_user.get_rol() != 'encargado':
            current_app.logger.info(f"Acceso prohibido a la ruta {request.path}")
            abort(403)  # Acceso prohibido si no es un alumno
        return func(*args, **kwargs)
    return decorated_view
