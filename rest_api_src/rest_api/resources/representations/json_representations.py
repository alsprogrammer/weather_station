from flask_restful import fields

pressure_measurement_repr = {
    'timestamp': fields.Integer,
    'value': fields.Integer
}
