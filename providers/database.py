from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
db = SQLAlchemy()

def init_db(app):
    #producción    Usuario: josue   Contrasña: 12345
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://tostadaconfrijol_SQLLogin_1:kd21j7pfk8@proyectobd.mssql.somee.com/proyectobd?driver=ODBC+Driver+17+for+SQL+Server'
    #desarrollo
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://proyectod:12345@PC-TOSTADACONFR/proyectobd?driver=ODBC+Driver+17+for+SQL+Server'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    