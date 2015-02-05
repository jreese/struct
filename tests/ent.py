# Copyright 2015 John Reese
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

from ent import Ent


class TestEnt(unittest.TestCase):

    def setUp(self):
        self.structure = {
            "scalar": 1,
            "list": [1, 2, 3, 4],
            "hash": {
                "scalar": 1,
                "list": [1, 2, 3, 4],
                "hash": {
                    "scalar": 1,
                }
            },
            "hashes": [
                {
                    "scalar": 1,
                    "list": [1, 2, 3, 4],
                    "hash": {
                        "scalar": 1,
                    }
                },
                {
                    "scalar": 1,
                    "list": [1, 2, 3, 4],
                    "hash": {
                        "scalar": 1,
                    }
                },
            ]
        }

    def test_attributes(self):
        ent = Ent.load(self.structure)

        self.assertEqual(ent.scalar, 1)

        self.assertIsInstance(ent.list, list)
        self.assertEqual(len(ent.list), 4)
        self.assertEqual(ent.list[2], 3)

        self.assertIsInstance(ent.hash, Ent)

        self.assertIsInstance(ent.hashes, list)
        self.assertEqual(len(ent.hashes), 2)
        self.assertIsInstance(ent.hashes[0], Ent)

    def test_nesting(self):
        ent = Ent.load(self.structure)

        self.assertEqual(ent.hash.scalar, 1)
        self.assertEqual(len(ent.hash.list), 4)
        self.assertEqual(ent.hash.list[2], 3)
        self.assertEqual(ent.hash.hash.scalar, 1)

        self.assertEqual(ent.hashes[0].scalar, 1)
        self.assertEqual(ent.hashes[0].list[1], 2)
        self.assertEqual(ent.hashes[1].hash.scalar, 1)

    def test_constructor_vs_load(self):
        ent1 = Ent(self.structure)
        ent2 = Ent.load(self.structure)

        self.assertEqual(ent1.scalar, ent2.scalar)
        self.assertEqual(ent1.list, ent2.list)

        self.assertEqual(ent1.hash.scalar, ent2.hash.scalar)
        self.assertEqual(ent1.hash.list, ent2.hash.list)
        self.assertEqual(ent1.hash.hash.scalar, ent2.hash.hash.scalar)

        self.assertEqual(ent1.hashes[0].scalar, ent2.hashes[0].scalar)
        self.assertEqual(ent1.hashes[0].list, ent2.hashes[0].list)
        self.assertEqual(ent1.hashes[0].hash.scalar,
                         ent2.hashes[0].hash.scalar)

        self.assertEqual(ent1.hashes[1].scalar, ent2.hashes[1].scalar)
        self.assertEqual(ent1.hashes[1].list, ent2.hashes[1].list)
        self.assertEqual(ent1.hashes[1].hash.scalar,
                         ent2.hashes[1].hash.scalar)

    @unittest.expectedFailure
    def test_dict_access(self):
        ent = Ent.load(self.structure)

        self.assertEqual(len(ent.hash), 3)
        self.assertTrue('scalar' in ent.hash)
