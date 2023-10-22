from providers.database import db
class Pago(db.Model):
    id_pago = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
