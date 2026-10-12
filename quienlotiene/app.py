from flask import Flask, request, jsonify
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quienlotiene.db'
db.init_app(app)

class Oferta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    solicitud_id = db.Column(db.Integer, db.ForeignKey('solicitud.id'))
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'))
    descripcion = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'Oferta({self.id}, {self.solicitud_id}, {self.proveedor_id}, {self.descripcion})'

@app.route('/oferta', methods=['POST'])
def crear_oferta():
    nueva_oferta = Oferta(
        solicitud_id=request.json['solicitud_id'],
        proveedor_id=request.json['proveedor_id'],
        descripcion=request.json['descripcion']
    )
    db.session.add(nueva_oferta)
    db.session.commit()
    return jsonify({'mensaje': 'Oferta creada con exito'}), 201
