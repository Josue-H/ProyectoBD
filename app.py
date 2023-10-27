from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, current_user
from auth.auth_views import auth
from sqlalchemy import and_ 
from sqlalchemy.orm import aliased, session,  joinedload
from models.usuario import Usuario
from models.grado import Grado
from models.rol import Rol 
from models.asignacion_rol import AsignacionRol
from models.administrador import Administrador
from models.alumno import Alumno
from models.profesor import Profesor
from models.curso import Curso
from models.inscripcion import Inscripcion
from models.encargado import Encargado
from models.pago import Pago
from models.asignacion import Asignacion
from models.colegiatura import Colegiatura
from models.nota import Nota
from models.asignacion_cur import AsignacionCur
from werkzeug.security import generate_password_hash
from providers.database import init_db, db # Importa init_db desde providers.database
from decorators import admin_required, teacher_required, student_required, encargado_required  # Importa los decoradores

app = Flask(__name__)
app.secret_key = '123MGJ456'
# Inicializa la base de datos pasando la aplicación Flask
init_db(app)

# Inicializar el administrador de inicio de sesión
login_manager = LoginManager()
login_manager.init_app(app)

# Función para cargar un usuario por su ID
@login_manager.user_loader
def load_user(user_id):
    usuario = Usuario.query.get(int(user_id))
    if usuario:
        # Verificar si el usuario es administrador
        if usuario.get_rol() == 'administrador':
            administrador = Administrador.query.filter_by(id_usuario=usuario.id_usuario).first()
            if administrador:
                usuario.administrador = administrador
        # Verificar si el usuario es profesor
        elif usuario.get_rol() == 'profesor':
            profesor = Profesor.query.filter_by(id_usuario=usuario.id_usuario).first()
            if profesor:
                usuario.profesor = profesor
        elif usuario.get_rol() == 'alumno':
            alumno = Alumno.query.filter_by(id_usuario=usuario.id_usuario).first()
            if alumno:
                usuario.alumno = alumno
        elif usuario.get_rol() == 'encargado':
            encargado = Encargado.query.filter_by(id_usuario=usuario.id_usuario).first()
            if encargado:
                usuario.encargado = encargado
    return usuario


# Registrar las rutas de autenticación
app.register_blueprint(auth, url_prefix='/')

# Ruta principal
@app.route('/')
def index():
    
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
     return render_template('error/404.html'), 404

# # Manejo de error 403 (Acceso prohibido)
@app.errorhandler(403)
def forbidden(error):
    return render_template('error/403.html'), 403

# Decorador para proteger una ruta que solo los administradores pueden acceder
@app.route('/admin')
@admin_required
def admin_dashboard():
    return render_template('admin/admin_dashboard.html', current_user=current_user)

@app.route('/admin/crear_grado', methods=['POST'])
@admin_required
def crear_grado():
    if request.method == 'POST':
        id_grado = request.form.get('id_grado')
        descripcion = request.form.get('descripcion')
        # Crea un nuevo grado en la base de datos
        nuevo_grado = Grado(id_grado=id_grado, descripcion=descripcion)
        db.session.add(nuevo_grado)
        db.session.commit()

        # Redirecciona de vuelta al panel de administración
        return redirect(url_for('admin_dashboard'))


@app.route('/admin/usuarios', methods=['GET', 'POST'])
@admin_required
def admin_usuarios():
    roles = Rol.query.all()
    if request.method == 'POST':
        
        id_usuario = request.form.get('id_usuario')
        usuario = request.form.get('usuario')
        contraseña = generate_password_hash(request.form.get('contraseña'))
        id_rol = request.form.get('rol')


        rol = Rol.query.filter_by(id_rol=id_rol).first()
        if not rol:
            # Maneja el caso en el que el id_rol no exista en la tabla de roles.
            flash('Rol no válido', 'error')
            return redirect('/admin/usuarios')
        
        # Crea una nueva instancia de Usuario.
        new_user = Usuario(id_usuario=id_usuario, usuario=usuario, contraseña=contraseña)
        # Agrega el usuario a la base de datos.
        db.session.add(new_user)
        db.session.commit()
        
        # Asigna el rol al usuario en la tabla AsignacionRol.
        rol_asign = AsignacionRol(id_usuario=new_user.id_usuario, id_rol=id_rol)
        db.session.add(rol_asign)
        db.session.commit()

        descripcion_rol = rol.descripcion
        
        if descripcion_rol == 'administrador':
            id_administrador = request.form.get('id_administrador')
            nombre_admin = request.form.get('nombre_admin')
            apellido_admin = request.form.get('apellido_admin')

            new_admin = Administrador(id_administrador = id_administrador, nombre = nombre_admin, apellido = apellido_admin, id_usuario = id_usuario)
            db.session.add(new_admin)
            db.session.commit()
            
            return redirect('/admin/usuarios')

        elif descripcion_rol == 'alumno':
            id_alumno = request.form.get('id_alumno')
            nombre_alumno = request.form.get('nombre_alumno')
            apellido_alumno = request.form.get('apellido_alumno')
            fecha_nac_alumno = request.form.get('fecha_nac_alum')
            genero  = request.form.get('genero')
         
            new_student = Alumno(id_alumno = id_alumno, nombre = nombre_alumno, apellido = apellido_alumno, fecha_nacimiento = fecha_nac_alumno, genero = genero, id_usuario = id_usuario)
            db.session.add(new_student)
            db.session.commit()

            return redirect('/admin/usuarios')
        
        elif descripcion_rol == 'profesor':
            id_profesor = request.form.get('id_profesor')
            nombre_profesor = request.form.get('nombre_profesor')
            apellido_profesor = request.form.get('apellido_profesor')
            profesion = request.form.get('profesion')

            new_teacher = Profesor(id_profesor = id_profesor, nombre = nombre_profesor, apellido = apellido_profesor, profesion = profesion, id_usuario = id_usuario)
            db.session.add(new_teacher)
            db.session.commit()

            return redirect('/admin/usuarios')

        elif descripcion_rol == 'encargado':
            id_encargado = request.form.get('id_encargado')
            nombre_encargado = request.form.get('nombre_encargado')
            telefono = request.form.get('telefono')
            direccion = request.form.get('direccion')
            correo = request.form.get('correo')

            new_incharge = Encargado(id_encargado = id_encargado, nombre = nombre_encargado, telefono = telefono, direccion = direccion, correo = correo, id_usuario = id_usuario)
            db.session.add(new_incharge)
            db.session.commit()

            return redirect('/admin/usuarios')

    return render_template('admin/admin_usuarios.html', roles=roles)

# Ruta para gestionar cursos
@app.route('/admin/cursos', methods=['GET', 'POST'])
@admin_required
def admin_cursos():
    profesores = Profesor.query.all()
    grados = Grado.query.all()
    cursos = Curso.query.all()
    if request.method == 'POST':
        button_id = request.form['submit-button']

        if button_id == 'crear_curso':
            id_curso = request.form.get('id_curso')
            descripcion = request.form.get('descripcion_curso')
            id_grado = request.form.get('grado')

            # Verificar si el código del curso ya existe en la base de datos
            curso_existente = Curso.query.filter_by(id_curso=id_curso).first()

            if curso_existente:
                # El código del curso ya existe, mostrar un mensaje de error
                flash('El código del curso ya está en uso. Ingrese uno diferente.', 'error')
            else:
                # El código del curso es único, guardar el curso en la base de datos
                new_course = Curso(id_curso=id_curso, descripcion=descripcion, id_grado=id_grado)
                db.session.add(new_course)
                db.session.commit()
                return redirect('/admin/cursos')
            
        elif button_id == 'asignar_curso':
            cursos = Curso.query.all()
            id_profesor = request.form.get('profesor')
            curso_id = request.form.get('curso')
            seccion = request.form.get('seccion')

            new_asig_cur = AsignacionCur(id_profesor= id_profesor, id_curso = curso_id, seccion = seccion)
            db.session.add(new_asig_cur)
            db.session.commit()
            return redirect('/admin/cursos')


    return render_template('admin/admin_cursos.html', profesores = profesores, grados = grados, cursos = cursos)

@app.route('/admin/inscripciones', methods=[ 'GET','POST'])
@admin_required
def admin_inscripciones():
    alumnos = Alumno.query.all()
    cursos = Curso.query.all()
    inscripciones = Inscripcion.query.all()
    encargados = Encargado.query.all()

    if request.method == 'POST':
        button_id = request.form['submit_button_id']

        if button_id == 'guardarAsignaciones':
            id_alumno = request.form.get('id_alumno_asign')
            id_curso = request.form.get('id_curso')
            id_inscripcion = request.form.get('id_inscripcion_asign')

            new_assig = Asignacion(id_alumno = id_alumno, id_curso = id_curso, id_inscripcion = id_inscripcion)
            db.session.add(new_assig)
            db.session.commit()
            return redirect('/admin/inscripciones')
        
        elif button_id == 'guardarInscripciones':
            fecha_insc = request.form.get('fecha_inscripcion')
            id_alumno = request.form.get('id_alumno_insc')
            id_encargado = request.form.get('encargado')
            id_pago = request.form.get('id_pago_insc')
            fecha_pago = request.form.get('fecha_pago_insc')

            new_pay = Pago(id_pago = id_pago, fecha = fecha_pago)
            db.session.add(new_pay)
            db.session.commit()

            new_insc = Inscripcion(fecha = fecha_insc, id_alumno = id_alumno, id_encargado = id_encargado, id_pago = id_pago)
            db.session.add(new_insc)
            db.session.commit()
            return redirect('/admin/inscripciones')
        

        elif button_id == 'guardarColegiaturas':
            fecha_col = request.form.get('fecha_colegiatura')
            id_alumno = request.form.get('id_alumno_col')
            id_inscripcion = request.form.get('id_inscripcion_col')
            id_pago = request.form.get('id_pago_col')
            fecha_pago = request.form.get('fecha_pago_col')

            new_pay = Pago(id_pago = id_pago, fecha = fecha_pago)
            db.session.add(new_pay)
            db.session.commit()

            new_col = Colegiatura( fecha = fecha_col, id_alumno = id_alumno, id_pago = id_pago, id_inscripcion = id_inscripcion)
            db.session.add(new_col)
            db.session.commit()
            return redirect('/admin/inscripciones')

    return render_template('admin/admin_inscripciones.html', alumnos = alumnos, cursos = cursos, inscripciones = inscripciones, encargados = encargados)


@app.route('/admin/notas', methods=[ 'GET'])
@admin_required
def gestionar_notas():

    alumnos = Alumno.query.all()

    return render_template('admin/admin_notas.html', alumnos=alumnos)

@app.route('/admin/guardar_nota', methods=['POST'])
@admin_required
def guardar_nota():
    alumno_id = request.form.get('alumno_id')
    curso_id = request.form.get('curso_id')
    nota = request.form.get('nota')
    print(alumno_id)
    # Validar si ya existe una nota para el mismo alumno y curso
    nota_existente = Nota.query.filter_by(id_alumno=alumno_id, id_curso=curso_id).first()

    if nota_existente:
        response = {'success': False, 'message': 'Ya existe una nota para este alumno y curso.'}
    else:
        nueva_nota = Nota(id_alumno=alumno_id, id_curso=curso_id, nota=nota)
        db.session.add(nueva_nota)
        db.session.commit()
        response = {'success': True, 'message': 'Nota guardada con éxito.'}

    return jsonify(response)

@app.route('/admin/cargar_cursos', methods=['POST'])
@admin_required
def cargar_cursos():
    alumno_id = request.form.get('alumno_id')
    if alumno_id:
        # Consultar los cursos del alumno
        cursos = Curso.query.join(Asignacion, and_(Curso.id_curso == Asignacion.id_curso, Asignacion.id_alumno == alumno_id)).all()
        # Consultar las notas del alumno
        notas = Nota.query.filter_by(id_alumno=alumno_id).all()

        # Preparar los datos para enviar como respuesta
        cursos_data = [{'id_curso': curso.id_curso, 'descripcion': curso.descripcion} for curso in cursos]
        notas_data = [{'id_curso': nota.id_curso, 'nota': nota.nota} for nota in notas]

        return jsonify({'cursos': cursos_data, 'notas': notas_data})
    
    return jsonify({'cursos': [], 'notas': []})


@app.route('/admin/profesores', methods=['GET'])
@admin_required
def listar_profesores():
    # Aquí recuperaríamos la lista de profesores y cursos asignados desde la base de datos
    # Debes adaptar esta parte según la estructura de tu base de datos
    profesores = Profesor.query.all()
    cursos = Curso.query.all()

    return render_template('admin/admin_profesores.html', profesores=profesores, cursos=cursos)

@app.route('/admin/obtener_cursos', methods=['POST'])
@admin_required
def obtener_cursos():
    # Obtener los parámetros de la solicitud POST
    profesor_id = request.form.get('profesor_id')
    grado_filter = request.form.get('grado_filter')
    seccion_filter = request.form.get('seccion_filter')

    # Recupera el profesor de la base de datos
    profesor = Profesor.query.get(profesor_id)

    if profesor is None:
        return jsonify({'error': 'Profesor no encontrado'})

    # Filtra las asignaciones de cursos para este profesor
    asignaciones = AsignacionCur.query.filter_by(id_profesor=profesor.id_profesor)

    # Aplica los filtros de grado y sección si se proporcionan
    if grado_filter:
        grado_filter_obj = Grado.query.filter_by(descripcion=grado_filter).first()
        if grado_filter_obj is None:
            return jsonify({'error': 'Grado no encontrado'})
        asignaciones = asignaciones.filter(AsignacionCur.curso.has(grado=grado_filter_obj))

    if seccion_filter:
        asignaciones = asignaciones.filter_by(seccion=seccion_filter)

    # Convierte las asignaciones en una lista de diccionarios
    cursos_filtrados = []
    for asignacion in asignaciones:
        curso = asignacion.curso
        curso_dict = {
            'profesor': f'{profesor.nombre} {profesor.apellido}',
            'curso': curso.descripcion,
            'grado': curso.grado.descripcion,
            'seccion': asignacion.seccion
        }
        cursos_filtrados.append(curso_dict)

    # Devuelve los cursos filtrados como respuesta en formato JSON
    return jsonify(cursos_filtrados)



@app.route('/profesor')
@teacher_required
def teacher_dashboard():
    return render_template('profesor/profesor_dashboard.html', current_user=current_user)

@app.route('/profesor/notas', methods=['GET', 'POST'])
@teacher_required
def profesor_notas():
    if request.method == 'POST':
        # Obten los datos del formulario
        curso_id = request.form.get('curso_id')
        alumno_id = request.form.get('alumno_id')
        nota_valor = request.form.get('nota_valor')

        # Crea un nuevo objeto Nota y guárdalo en la base de datos
        nota = Nota(id_alumno=alumno_id,id_curso=curso_id,  nota=nota_valor)
        db.session.add(nota)
        db.session.commit()

        return redirect(('/profesor/notas'))

    # Si es una solicitud GET, renderiza el formulario
    cursos_asignados = AsignacionCur.query.filter_by(id_profesor=current_user.profesor.id_profesor).all()
    return render_template('profesor/profesor_notas.html', cursos_asignados=cursos_asignados)

@app.route('/profesor/obtener_alumnos', methods=['POST', 'GET'])
@teacher_required
def obtener_alumnos():
    if request.method == 'POST':
        curso_id = request.form.get('curso_id')
        # Realiza la lógica para obtener los alumnos asignados a ese curso
        alumnos = Alumno.query.join(Asignacion, Alumno.id_alumno == Asignacion.id_alumno)\
            .filter(Asignacion.id_curso == curso_id).all()

        # Convierte los datos de los alumnos a un formato adecuado
        alumnos_data = [{"id_alumno": alumno.id_alumno, "nombre": alumno.nombre, "apellido": alumno.apellido} for alumno in alumnos]

        return jsonify({"alumnos": alumnos_data})
    
@app.route('/profesor/obtener_nota', methods=['POST'])
@teacher_required
def obtener_nota():
        curso_id = request.form.get('curso_id')
        alumno_id = request.form.get('alumno_id')
        nota_existente = Nota.query.filter_by(id_alumno=alumno_id, id_curso=curso_id).first()
        if nota_existente:
         return jsonify({"nota": nota_existente.nota})
        else:
            return jsonify({"nota": None})

@app.route('/profesor/cursos', methods=['GET'])
@teacher_required
def cursos():

    cursos = Curso.query.join(AsignacionCur, and_(Curso.id_curso == AsignacionCur.id_curso, AsignacionCur.id_profesor == current_user.profesor.id_profesor)).all()
    # Lógica para manejar la ruta de cursos
    return render_template('profesor/profesor_cursos.html', cursos = cursos)

# Ruta para obtener las secciones de un curso
@app.route('/profesor/obtener_secciones', methods=['POST'])
@teacher_required
def obtener_secciones():
    curso_id = request.form.get('curso_id')
    profesor_id = current_user.profesor.id_profesor
    
    # Aquí debes realizar la consulta a la base de datos para obtener las secciones del curso
    # relacionadas con el profesor (usando los modelos Profesor, AsignacionCur y Curso)
    secciones = db.session.query(AsignacionCur.seccion).filter(
        AsignacionCur.id_profesor == profesor_id, AsignacionCur.id_curso == curso_id
    ).distinct().all()

    secciones = [seccion[0] for seccion in secciones]

    return jsonify({'secciones': secciones})

# Ruta para obtener la información de los alumnos según el curso y la sección
@app.route('/profesor/obtener_alumnos_filtrados', methods=['POST'])
@teacher_required
def obtener_alumnos_seccion():
    curso_id = request.form.get('curso_id')
    seccion = request.form.get('seccion')
    query = (
        db.session.query(AsignacionCur)
        .join(Curso)
        .filter(AsignacionCur.id_curso == curso_id)
    )
    if seccion:
        query = query.filter(AsignacionCur.seccion == seccion)

    asignaciones = query.all()

    alumnos_data = []
    
    for asignacion in asignaciones:
        # Verificar si hay asignaciones de cursos
        if asignacion.curso.asignaciones_curso:
            alumno = asignacion.curso.asignaciones_curso[0].alumno
            alumnos_data.append({
                "id_alumno": alumno.id_alumno,
                "nombre": alumno.nombre,
                "apellido": alumno.apellido,
                "grado": asignacion.curso.grado.descripcion,
                "seccion": asignacion.seccion
            })

    return jsonify({"alumnos": alumnos_data})

@app.route('/alumno', methods=['GET'])
@student_required
def student_dashboard():
   # Obtener el alumno logueado
    #Obtener el alumno logueado
    alumno = Alumno.query.filter_by(id_usuario=current_user.id_usuario).first()

    # Consultar todas las asignaciones del alumno con información adicional
    asignaciones = Asignacion.query.filter_by(id_alumno=alumno.id_alumno).all()
    cursos = {asignacion.curso.id_curso: asignacion.curso.descripcion for asignacion in asignaciones}
    return render_template('alumno/alumno_dashboard.html', asignaciones=asignaciones, current_user=current_user, cursos=cursos)

@app.route('/encargado', methods=['GET'])
@encargado_required
def encargado_dashboard():
    # Obtener el usuario encargado logueado
    encargado = Encargado.query.filter_by(id_usuario=current_user.id_usuario).first()
    
    # Consultar todos los alumnos asignados al encargado
    alumnos_asignados = encargado.inscripciones
    return render_template('encargado/encargado_dashboard.html', alumnos_asignados=alumnos_asignados, current_user=current_user)

@app.route('/encargado/alumno_info', methods=['GET'])
@encargado_required
def get_alumno_info():
    alumno_id = request.args.get('alumno_id')
    
    # Obtener la información del alumno seleccionado
    alumno = Alumno.query.get(alumno_id)
    asignaciones = Asignacion.query.filter_by(id_alumno=alumno_id).all()
    
    # Preparar los datos para enviar al navegador
    data = {
        'alumno_nombre': f'{alumno.nombre} {alumno.apellido}',
        'asignaciones': []
    }
    for asignacion in asignaciones:
        data['asignaciones'].append({
            'curso': asignacion.curso.descripcion,
            'profesor': f'{asignacion.curso.asignaciones[0].profesor.nombre} {asignacion.curso.asignaciones[0].profesor.apellido}',
            'nota': asignacion.curso.nota[0].nota if asignacion.curso.nota else 'Nota no ingresada'
        })

    return jsonify(data)


if __name__ == '__main__':
    app.run()
