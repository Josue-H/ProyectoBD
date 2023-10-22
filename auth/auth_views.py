from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models.usuario import Usuario

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Usuario.query.filter_by(usuario=username).first()

        if user :
           # print(user)
            if user.check_password(password):
                login_user(user)
                flash('Inicio de sesión exitoso', 'success')
                # Obtener el rol del usuario
                rol = user.get_rol()
                print(f'Rol del usuario: {rol}')
                # Redirigir al usuario según su rol
                if rol == 'administrador':
                    return redirect(url_for('admin_dashboard'))
                elif rol == 'alumno':
                    return redirect(url_for('student_dashboard'))
                elif rol == 'profesor':
                    return redirect(url_for('teacher_dashboard'))
                elif rol == 'encargado':
                    return redirect(url_for('encargado_dashboard'))
                else:
                    flash('Rol desconocido', 'danger')

            else:
                flash('Credenciales inválidas', 'danger')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Cierre de sesión exitoso', 'success')
    return redirect(url_for('auth.login'))

