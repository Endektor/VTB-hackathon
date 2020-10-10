import ast

from rest_framework.response import Response
from rest_framework.views import APIView

import base64
import http.client
import json


# class CarNameGetter(APIView):
#
#     def post(self, request):
#         return Response(self.get_car_name(request))
#
#     @staticmethod
#     def get_car_name(request):
#         conn = http.client.HTTPSConnection("gw.hackathon.vtb.ru")
#         data = {"content": base64.encodebytes(open('Hyundai_Genesis.jpg', 'rb').read()).decode('UTF-8').replace('\n', '')}
#
#         payload = json.dumps(data)
#
#         headers = {
#             'x-ibm-client-id': "744a2a505e92e8b783a40224d6230be2",
#             'content-type': "application/json",
#             'accept': "application/json"
#         }
#
#         conn.request("POST", "/vtb/hackathon/car-recognize", payload, headers)
#
#         res = conn.getresponse()
#         data = res.read()
#
#         print(data.decode("utf-8"))


class SettingsGetter(APIView):

    def get(self, request):
        return Response(self.get_settings(request))

    @staticmethod
    def get_settings(request):
        conn = http.client.HTTPSConnection("gw.hackathon.vtb.ru")

        with open('client_id.txt', 'r') as f:
            client_id = f.read()

        headers = {
            'x-ibm-client-id': client_id,
            'accept': "application/json"
        }

        conn.request("GET", "/vtb/hackathon/settings?name=Haval&language=en", headers=headers)

        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")


class CalculationsGetter(APIView):

    def post(self, request):
        return Response(self.get_calculations(request))

    @staticmethod
    def get_calculations(request):
        conn = http.client.HTTPSConnection("gw.hackathon.vtb.ru")

        payload = {"clientTypes": ["ac43d7e4-cd8c-4f6f-b18a-5ccbc1356f75"],
                   "cost": 850000, "initialFee": 200000, "kaskoValue": 10000,
                   "language": "en", "residualPayment": 0, "settingsName": "Haval",
                   "specialConditions": ["57ba0183-5988-4137-86a6-3d30a4ed8dc9",
                                         "b907b476-5a26-4b25-b9c0-8091e9d5c65f",
                                         "cbfc4ef3-af70-4182-8cf6-e73f361d1e68"],
                   "term": 5}
        payload_json = json.dumps(payload)

        with open('client_id.txt', 'r') as f:
            client_id = f.read()

        headers = {
            'x-ibm-client-id': client_id,
            'content-type': "application/json",
            'accept': "application/json"
        }

        conn.request("POST", "/vtb/hackathon/calculate", payload_json, headers)

        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")


class CarLoan(APIView):

    def post(self, request):
        return Response(self.post_car_loan(request))

    @staticmethod
    def post_car_loan(request):
        conn = http.client.HTTPSConnection("gw.hackathon.vtb.ru")

        payload = {"comment": "Комментарий",
                   "customer_party": {"email": "apetrovich@example.com",
                                      "income_amount": 140000,
                                      "person": {"birth_date_time": "1981-11-01",
                                                 "birth_place": "г. Воронеж", "family_name": "Иванов",
                                                 "first_name": "Иван", "gender": "male", "middle_name": "Иванович",
                                                 "nationality_country_code": "RU"}, "phone": "+99999999999"},
                   "datetime": "2020-10-10T08:15:47Z", "interest_rate": 15.7, "requested_amount": 300000,
                   "requested_term": 36, "trade_mark": "Nissan", "vehicle_cost": 600000}
        payload_json = json.dumps(payload)

        with open('client_id.txt', 'r') as f:
            client_id = f.read()

        headers = {
            'x-ibm-client-id': client_id,
            'content-type': "application/json",
            'accept': "application/json"
        }

        conn.request("POST", "/vtb/hackathon/carloan", payload_json, headers)

        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")


class CarGetter(APIView):

    def post(self, request):

        return Response(self.get_cars(request))
    
    @staticmethod
    def get_cars(request):
        conn = http.client.HTTPSConnection("gw.hackathon.vtb.ru")
        data = {"content": base64.encodebytes(open('123.jpg', 'rb').read()).decode('UTF-8').replace('\n', '')}

        payload = json.dumps(data)

        with open('client_id.txt', 'r') as f:
            client_id = f.read()

        headers = {
            'x-ibm-client-id': client_id,
            'content-type': "application/json",
            'accept': "application/json"
        }

        conn.request("POST", "/vtb/hackathon/car-recognize", payload, headers)

        res = conn.getresponse()
        data_1 = res.read().decode("utf-8")

        conn.request("GET", "/vtb/hackathon/marketplace", headers=headers)

        res = conn.getresponse()
        data_2 = res.read().decode('utf-8')

        data_2_obj = json.loads(data_2)
        carListValues = list(ast.literal_eval(data_1)['probabilities'].values())
        carList = ast.literal_eval(data_1)['probabilities']
        carListEnd = list()
        for el in carListValues:
            carListEnd.append(float(el))
        carListEnd = sorted(carListEnd, reverse=True)

        hardcode = {
            "BMW 3": [15, 2],
            "BMW 5": [15, 4],
            "Cadillac ESCALADE": [18, 0],
            "Chevrolet Tahoe": [16, 1],
            "Hyundai Genesis": '',
            "Jaguar F-PACE": [13, 4],
            "KIA K5": [2, 9],
            "KIA Optima": [2, 8],
            "KIA Sportage": [2, 7],
            "Land Rover RANGE ROVER VELAR": [17, 2],
            "Mazda 3": '',
            "Mazda 6": [12, 1],
            "Mercedes A": '',
            "Toyota Camry": ''
        }

        cars = {
            "currency": {
                "usd": "",
                "eur": "",
                "doshirak": 40
            },
            "list": []
        }

        for f in range(len(carListEnd)):
            carName = list(carList.keys())[list(carList.values()).index(carListEnd[f])]

            if hardcode[carName] != '':
                i = hardcode[carName][0]
                j = hardcode[carName][1]

                tempCar = {
                    "title": data_2_obj['list'][i]['title'],
                    "model": data_2_obj['list'][i]['models'][j]['title'],
                    "colors": data_2_obj['list'][i]['models'][j]['colorsCount'],
                    "doors": data_2_obj['list'][i]['models'][j]['bodies'][0]['doors'],
                    "type": data_2_obj['list'][i]['models'][j]['bodies'][0]['type'],
                    "logo": data_2_obj['list'][i]['logo'],
                    "photo": data_2_obj['list'][i]['models'][j]['photo'],
                    "price": data_2_obj['list'][i]['models'][j]['minprice'],
                }

                cars['list'].append(tempCar)

        carsListTemp = list()
        for k in range(3):
            carsListTemp.append(cars['list'][k])

        return json.dumps(carsListTemp)
