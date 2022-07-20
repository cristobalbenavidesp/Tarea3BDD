import flask
import datetime
from flask import Flask, jsonify, request
from config import config
from models import db, Persona, Factura, Reproduccion, Cancion

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def create_app(environment):
    app = Flask(__name__)
    app.config["JSON_AS_ASCII"] = False
    app.config.from_object(environment)
    with app.app_context():
        db.init_app(app)
        db.create_all()
    return app


environment = config['development']
app = create_app(environment)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Mi primera API :P</h1>"

# READ


@app.route('/personas', methods=['GET'])
def getPersonas():
    personas = [persona.json() for persona in Persona.query.all()]
    return jsonify(personas)


@app.route('/facturas', methods=['GET'])
def getFacturas():
    facturas = [factura.json() for factura in Factura.query.all()]
    return jsonify(facturas)


@app.route('/canciones', methods=['GET'])
def getCanciones():
    canciones = [cancion.json() for cancion in Cancion.query.all()]
    return jsonify(canciones)


@app.route('/reproducciones', methods=['GET'])
def getReproducciones():
    reproducciones = [reproduccion.json()
                      for reproduccion in Reproduccion.query.all()]
    return jsonify(reproducciones)

# DELETE


@app.route('/personas/<id>', methods=['DELETE'])
def borrar_persona(id):
    persona = Persona.query.filter_by(id=id).first()
    persona.delete()
    return "<h1>Usuario eliminado </h1>"


@app.route('/facturas/<id>', methods=['DELETE'])
def borrar_factura(id):
    factura = Factura.query.filter_by(id=id).first()
    factura.delete()
    return "<h1>Usuario eliminado </h1>"


@app.route('/canciones/<id>', methods=['DELETE'])
def borrar_cancion(id):
    cancion = Cancion.query.filter_by(id=id).first()
    cancion.delete()
    return "<h1>Usuario eliminado </h1>"

# CREATE


@app.route('/personas/<id>', methods=['POST'])
def crear_persona(id):

    request_body = request.json
    persona = Persona(id=id, nombre=request_body["nombre"], apellido=request_body["apellido"],
                      email=request_body["email"], password=request_body["password"],
                      artista_nombre_artistico=request_body["artista_nombre_artistico"],
                      usuario_suscripcion_activa=request_body["usuario_suscripcion_activa"],
                      artista_verificado=request_body["artista_verificado"], tipo_de_persona=request_body["tipo_de_persona"])
    persona.save()
    return jsonify(request_body)


@app.route('/facturas/<id>', methods=['POST'])
def crear_factura(id):

    request_body = request.json
    factura = Factura(id=id, monto_facturado=request_body["monto_facturado"],
                      fecha_facturacion=request_body["fecha_facturacion"],
                      fecha_vencimiento=request_body["fecha_vencimiento"],
                      estado=request_body["estado"],
                      metodo_de_pago=request_body["metodo_de_pago"],
                      fecha_hora_pago=request_body["fecha_hora_pago"],
                      id_usuario=request_body["id_usuario"])
    factura.save()
    return jsonify(request_body)


@app.route('/canciones/<id>', methods=['POST'])
def crear_cancion(id):

    request_body = request.json
    cancion = Cancion(id=id, nombre=request_body["nombre"],
                      letra=request_body["letra"],
                      fecha_composicion=request_body["fecha_composicion"])
    cancion.save()
    return jsonify(request_body)


@app.route('/reproducciones/<id_usuario>/<id_cancion>', methods=['POST'])
def crear_reproduccion(id_usuario, id_cancion):

    request_body = request.json
    reproduccion = Reproduccion(id_cancion=id_cancion, id_usuario=id_usuario,
                                cantidad_reproducciones=request_body["cantidad_reproducciones"],
                                ultima_reproduccion=request_body["ultima_reproduccion"])
    reproduccion.save()
    return jsonify(request_body)


# UPDATE


@app.route('/personas/<id>', methods=['PUT'])
def actualizar_persona(id):
    request_body = request.json
    persona = Persona.query.filter_by(id=id).first()
    personajson = persona.json()
    for i in request_body:
        personajson[i] = request_body[i]
    persona.jsonsave(personajson)
    return jsonify(personajson)


@app.route('/facturas/<id>', methods=['PUT'])
def actualizar_factura(id):
    request_body = request.json
    factura = Factura.query.filter_by(id=id).first()
    facturajson = factura.json()
    for i in request_body:
        facturajson[i] = request_body[i]
    factura.jsonsave(facturajson)
    return jsonify(facturajson)


@app.route('/cancion/<id>', methods=['PUT'])
def actualizar_cancion(id):
    request_body = request.json
    cancion = Cancion.query.filter_by(id=id).first()
    cancionjson = cancion.json()
    for i in request_body:
        cancionjson[i] = request_body[i]
    cancion.jsonsave(cancionjson)
    return jsonify(cancionjson)


@app.route('/reproducciones/<id_usuario>/<id_cancion>', methods=['PUT'])
def actualizar_reproduccion(id_usuario, id_cancion):
    request_body = request.json
    reproduccion = Reproduccion.query.filter_by(
        id_usuario=id_usuario, id_cancion=id_cancion).first()
    reproduccionjson = reproduccion.json()
    for i in request_body:
        reproduccionjson[i] = request_body[i]
    reproduccion.jsonsave(reproduccionjson)
    return jsonify(reproduccionjson)

# USUARIO MOROSO


@app.route('/personas/<id>/moroso', methods=['GET'])
def getPersona(id):
    vencidas = []
    personas = Persona.query.filter_by(id=id).first()
    facturas = [factura.json for factura in Factura.query.all()]
    current_time = datetime.datetime.now()
    for factura in facturas:
        if(comprobar_vencimiento(factura["fecha_vencimiento"])):
            vencidas.append(factura)
    if len(vencidas) == 0:
        return "Esta persona no tiene deudas!"
    else:
        return{
            "mensaje": "El usuario tiene facturas vencidas.",
            "facturas": jsonify(vencidas)
        }


app.run()
