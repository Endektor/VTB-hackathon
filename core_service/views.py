from datetime import datetime

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

import ast

import base64
import http.client
import json
from pycbrf.toolbox import ExchangeRates


class SettingsGetter(APIView):

    def get(self, request):
        return HttpResponse(self.get_settings(request))

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
        return HttpResponse(self.get_calculations(request))
        # return Response(self.get_calculations(request))

    @staticmethod
    def get_calculations(request):

        received_data = json.loads(request.body)

        conn = http.client.HTTPSConnection("gw.hackathon.vtb.ru")

        payload = {"clientTypes": ["ac43d7e4-cd8c-4f6f-b18a-5ccbc1356f75"],
                   "cost": received_data["cost"], "initialFee": received_data["initialFee"], "kaskoValue": 10000,
                   "language": "en", "residualPayment": 0, "settingsName": "Haval",
                   "specialConditions": received_data["specialConditions"],
                   "term": received_data["term"]}

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
        return HttpResponse(self.post_car_loan(request))

    @staticmethod
    def post_car_loan(request):
        conn = http.client.HTTPSConnection("gw.hackathon.vtb.ru")

        received_data = json.loads(request.body)

        payload = {"comment": "Комментарий",
                   "customer_party": {"email": received_data["email"],
                                      "income_amount": received_data["income_amount"],
                                      "person": {"birth_date_time": received_data["birth_date_time"],
                                                 "birth_place": received_data["birth_place"],
                                                 "family_name": received_data["family_name"],
                                                 "first_name": received_data["first_name"],
                                                 "gender": received_data["gender"],
                                                 "middle_name": received_data["middle_name"],
                                                 "nationality_country_code": "RU"}, "phone": received_data["phone"]},
                   "datetime": "2020-10-10T08:15:47Z", "interest_rate": 15.7,
                   "requested_amount": received_data["requested_amount"],
                   "requested_term": received_data["requested_term"], "trade_mark": received_data["trade_mark"],
                   "vehicle_cost": received_data["vehicle_cost"]}
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

        return HttpResponse(self.get_cars(request))
    
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

        d = datetime.today().strftime("%Y-%m-%d")
        rates = ExchangeRates(d)

        cars = {
            "currency": {
                "usd": rates['USD'].value,
                "eur": rates['EUR'].value,
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
                    "price": data_2_obj['list'][i]['models'][j]['minPrice'],
                }

                cars['list'].append(tempCar)

        carsListTemp = list()
        for k in range(3):
            carsListTemp.append(cars['list'][k])

        return json.dumps(carsListTemp)
