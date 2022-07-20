from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Persona(db.Model):
    __tablename__ = 'persona'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    artista_nombre_artistico = db.Column(db.String(100))
    usuario_suscripcion_activa = db.Column(db.Boolean)
    artista_verificado = db.Column(db.Boolean)
    tipo_de_persona = db.Column(db.Boolean, nullable=False)
    factura = db.relationship("Factura")
    reproduccion = db.relationship("Reproduccion")

    @classmethod
    def create(cls, nombre, apellido, email, password,
               artista_nombre_artistico,
               usuario_suscripcion_activa,
               artista_verificado, tipo_de_persona):
        persona = Persona(
            nombre=nombre,
            apellido=apellido,
            email=email, password=password,
            artista_nombre_artistico=artista_nombre_artistico,
            usuario_suscripcion_activa=usuario_suscripcion_activa,
            artista_verificado=artista_verificado,
            tipo_de_persona=tipo_de_persona)
        return persona.save()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False

    def update(self):
        self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def json(self):
        return{
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'artista_nombre_artistico': self.artista_nombre_artistico,
            'usuario_suscripcion_activa': self.usuario_suscripcion_activa,
            'artista_verificado': self.artista_verificado,
            'tipo_de_persona': self.tipo_de_persona
        }

    def jsonsave(self, file):
        self.nombre = file["nombre"]
        self.apellido = file['apellido']
        self.email = file["email"]
        self.artista_nombre_artistico = file["artista_nombre_artistico"]
        self.usuario_suscripcion_activa = file["usuario_suscripcion_activa"]
        self.artista_verificado = file["artista_verificado"]
        self.tipo_de_persona = file["tipo_de_persona"]
        self.save()


class Factura(db.Model):
    __tablename__ = 'factura'
    id = db.Column(db.Integer, primary_key=True)
    monto_facturado = db.Column(db.Integer)
    fecha_facturacion = db.Column(db.Integer)
    fecha_vencimiento = db.Column(db.String(8))
    estado = db.Column(db.Boolean)
    metodo_de_pago = db.Column(db.String(100))
    fecha_hora_pago = db.Column(db.Integer)
    id_usuario = db.Column(db.Integer, db.ForeignKey('persona.id'))

    @classmethod
    def create(cls, monto_facturado, fecha_facturacion, fecha_vencimiento,
               estado, metodo_de_pago, fecha_hora_pago, id_usuario):
        factura = Factura(
            monto_facturado=monto_facturado,
            fecha_facturacion=fecha_facturacion,
            fecha_vencimiento=fecha_vencimiento,
            estado=estado,
            metodo_de_pago=metodo_de_pago,
            fecha_hora_pago=fecha_hora_pago,
            id_usuario=id_usuario)
        return factura.save()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False

    def update(self):
        self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def json(self):
        return{
            'id': self.id,
            'monto_facturado': self.monto_facturado,
            'fecha_facturacion': self.fecha_facturacion,
            'fecha_vencimiento': self.fecha_vencimiento,
            'estado': self.estado,
            'metodo_de_pago': self.metodo_de_pago,
            'fecha_hora_pago': self.fecha_hora_pago,
            'id_usuario': self.id_usuario
        }

    def jsonsave(self, file):
        self.monto_facturado = file["monto_facturado"]
        self.fecha_facturacion = file["fecha_facturacion"]
        self.fecha_vencimiento = file["fecha_vencimiento"]
        self.estado = file["estado"]
        self.metodo_de_pago = file["metodo_de_pago"]
        self.fecha_hora_pago = file["fecha_hora_pago"]
        self.id_usuario = file["id_usuario"]
        self.save()


class Reproduccion(db.Model):
    __tablename__ = 'reproduccion'
    id_usuario = db.Column(db.Integer, db.ForeignKey(
        "persona.id"), primary_key=True)
    id_cancion = db.Column(db.Integer, db.ForeignKey(
        "cancion.id"), primary_key=True)
    cantidad_reproducciones = db.Column(db.Float, primary_key=True)
    ultima_reproduccion = db.Column(db.Integer, primary_key=True)

    @classmethod
    def create(cls, id_usuario, id_cancion, cantidad_reproducciones, ultima_reproduccion):
        reproduccion = Reproduccion(
            id_usuario=id_usuario,
            id_cancion=id_cancion,
            cantidad_reproducciones=cantidad_reproducciones,
            ultima_reproduccion=ultima_reproduccion)
        return reproduccion.save()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False

    def update(self):
        self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def json(self):
        return{
            'id_usuario': self.id_usuario,
            'id_cancion': self.id_cancion,
            'cantidad_reproducciones': self.cantidad_reproducciones,
            'ultima_reproduccion': self.ultima_reproduccion
        }

    def jsonsave(self, file):
        self.cantidad_reproducciones = file["cantidad_reproducciones"]
        self.ultima_reproduccion = file["ultima_reproduccion"]
        self.save()


class Cancion(db.Model):
    __tablename__ = 'cancion'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    letra = db.Column(db.String(300))
    fecha_composicion = db.Column(db.String(8))
    reproduccion = db.relationship("Reproduccion")

    @classmethod
    def create(cls, nombre, letra, fecha_composicion):
        cancion = Cancion(
            nombre=nombre,
            letra=letra,
            fecha_composicion=fecha_composicion)
        return cancion.save()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False

    def update(self):
        self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def json(self):
        return{
            'id': self.id,
            'nombre': self.nombre,
            'letra': self.letra,
            'fecha_composicion': self.fecha_composicion
        }

    def jsonsave(self, file):
        self.nombre = file["nombre"]
        self.letra = file["letra"]
        self.fecha_composicion = file["fecha_composicion"]
        self.save()
