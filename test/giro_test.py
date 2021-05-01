"""
author: Luis Manuel Torres Trevino
date: 30/04/2021
"""
import unittest
import json

from app import app


class GiroTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.headers = {"Content-Type": "application/json"}

    def test_create_giro(self):
        payload = {
            "uuid": "f7fb2473-abf1-4c7c-b17e-639dfc7bb20b-test",
            "giro": "test",
            "subtotal": "1000.00",
            "giro_impuesto_gravado": "1000.00",
            "giro_impuesto_exento": "0",
            "giro_otros_pagos": "0",
            "giro_iva": "0",
            "giro_retencion": "0",
            "giro_descuento": "240.98",
            "giro_total": "2061.60"
        }
        resp = self.app.post("/v1/giro/", headers=self.headers,
                             data=json.dumps({"giro": payload}))

        self.assertEqual(200, resp.status_code)
        self.assertEqual(True, resp.json["status"])

    def test_create_bulk_giro(self):
        payload = [
            {
                "uuid": "f7fb2473-abf1-4c7c-b17e-639dfc7bb20b-test",
                "giro": "test",
                "subtotal": "1000.00",
                "giro_impuesto_gravado": "1000.00",
                "giro_impuesto_exento": "0",
                "giro_otros_pagos": "0",
                "giro_iva": "0",
                "giro_retencion": "0",
                "giro_descuento": "240.98",
                "giro_total": "2061.60"
            },
            {
                "uuid": "f7fb2473-abf1-4c7c-b17e-639dfc7bb20b-test",
                "giro": "test",
                "subtotal": "1000.00",
                "giro_impuesto_gravado": "1000.00",
                "giro_impuesto_exento": "0",
                "giro_otros_pagos": "0",
                "giro_iva": "0",
                "giro_retencion": "0",
                "giro_descuento": "240.98",
                "giro_total": "2061.60"
            },
        ]
        resp = self.app.post("/v1/giro/bulk", headers=self.headers,
                             data=json.dumps({"documents": payload}))

        self.assertEqual(200, resp.status_code)
        self.assertEqual(True, resp.json["status"])

    def test_get_giro(self):
        payload = {
            "type": "and",
            "filters": {
                "uuid": "f7fb2473-abf1-4c7c-b17e-639dfc7bb20b-test"
            }
        }
        resp = self.app.get("/v1/giro/", headers=self.headers, data=json.dumps(payload))

        self.assertEqual(200, resp.status_code)
        self.assertEqual(True, resp.json["status"])
        self.assertEqual(payload["filters"]["uuid"], resp.json["data"]["uuid"])


if __name__ == '__main__':
    unittest.main()