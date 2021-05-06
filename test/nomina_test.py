"""
author: Luis Manuel Torres Trevino
date: 30/0472021
"""
import unittest
import json

from app import create_app


class NominaTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.headers = {"Content-Type": "application/json"}

    def test_find_nomina(self):
        payload = {"type": "and", "filters": {"datos.Rfc": "GPR070228780"}}
        resp = self.app.get(
            "/v1/nomina/", headers=self.headers, data=json.dumps(payload)
        )

        if resp.status_code == 404:
            self.assertEqual(404, resp.status_code)
            self.assertEqual(False, resp.json["status"])
        else:
            self.assertEqual(200, resp.status_code)
            self.assertEqual(True, resp.json["status"])

    def test_find_all_nomina(self):
        payload = {
            "type": "date",
            "filters": {
                "from_date": "2021-01-01",
                "to_date": "2021-01-04",
                "rfc": "GPR070228780",
            },
        }
        resp = self.app.get(
            "/v1/nomina/all", headers=self.headers, data=json.dumps(payload)
        )

        self.assertEqual(200, resp.status_code)
        self.assertEqual(True, resp.json["status"])
        self.assertGreater(len(resp.json["data"]), 0)
