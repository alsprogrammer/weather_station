from flask_restful import Resource, marshal

from rest_api_srv.rest_api.resources.representations.json_representations import pressure_measurement_repr
from rest_api_srv.rest_api.resources.parsers.pressure_parser import pressure_measurement_parser


class Pressure(Resource):
    def __init__(self, **kwargs):
        self._pressure_service = kwargs['pressure_service']

    def delete(self, timestamp: int):
        return {'status': 'ok'}


class PressureList(Resource):
    def __init__(self, **kwargs):
        self._pressure_service = kwargs['pressure_service']

    def get(self):
        measurements = self._pressure_service.get_last_n_measurements(24)
        return marshal(measurements, pressure_measurement_repr), 200

    def post(self):
        args = pressure_measurement_parser.parse_args()
        new_measurement = self._pressure_service.create_measurement(args['value'], args['timestamp'])
        return marshal(new_measurement, pressure_measurement_repr), 201
