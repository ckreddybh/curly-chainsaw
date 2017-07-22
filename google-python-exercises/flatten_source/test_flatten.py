#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import json

from flatten_json import flatten


class Test(unittest.TestCase):

    def setUp(self):
        f = open('expencted.json', 'w')
        f.write(json.dumps([{"account_number": "ABC15797531", "description": "Industrial Cleaning Supply Company", "name": "Xytrex Co.", "id": "1"}]))
        f.close()

    def runTest(self):
        with open('accounts.json') as json_data:
            d = json.load(json_data)
        flatten(d)
        with open('account.json') as json_data:
            f1 = json.load(json_data)
        with open('expencted.json') as json_data:
            f2 = json.load(json_data)
        self.assertEqual(f1, f2)

if __name__ == '__main__':
    unittest.main()
