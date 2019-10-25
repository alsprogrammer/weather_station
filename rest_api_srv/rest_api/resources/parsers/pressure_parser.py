from flask_restful import reqparse

pressure_measurement_parser = reqparse.RequestParser()
pressure_measurement_parser.add_argument('timestamp', type=int, help='The measurement timestamp')
pressure_measurement_parser.add_argument('value', type=int, help='The atmospheric pressure value', required=True)
