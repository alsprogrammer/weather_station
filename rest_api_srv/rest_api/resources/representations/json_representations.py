from flask_restful import fields

from utils.time_utils import get_current_timestamp

pressure_measurement_repr = {
    'timestamp': fields.Integer,
    'value': fields.Integer
}
