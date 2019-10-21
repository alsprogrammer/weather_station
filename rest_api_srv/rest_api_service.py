from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

from rest_api_srv.barometer.models import PressureMeasurement
from rest_api_srv.barometer.service import MeasurementService
from rest_api_srv.barometer.storages.SQLMeasurementStorage import SQLMeasurementStorage
from rest_api_srv.barometer.storages.sqlite_cursor import get_sqlite_cursor
from rest_api_srv.rest_api.resources.pressure import *


class RESTfulAPIService:
    def __init__(self, pressure_service: MeasurementService):
        self._pressure_service = pressure_service
        self.app = Flask(__name__, static_url_path='')
        self.api = Api(self.app)

        self.api.add_resource(PressureList, '/weather/api/v1.0/pressure',
                              resource_class_kwargs={'pressure_service': self._pressure_service})

    def start(self):
        self.app.run()


if __name__ == "__main__":
    db_cursor = get_sqlite_cursor(':memory:')
    db_cursor.execute('CREATE TABLE Pressure (timestamp INT, value INT);')
    db_cursor.execute('INSERT INTO Pressure VALUES (?, ?);', (946684800000, 735,))  # 2000-01-01 00:00:00
    db_cursor.execute('INSERT INTO Pressure VALUES (?, ?);', (1571633815310, 745,))  # 2000-01-01 00:00:00

    pressure_storage = SQLMeasurementStorage(db_cursor, 'Pressure', PressureMeasurement)
    pressure_service = MeasurementService(pressure_storage, PressureMeasurement)
    rest_service = RESTfulAPIService(pressure_service)
    rest_service.start()
