# -*- coding: utf-8 -*-

#       copyright (c) Notxor 2012

#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import unittest

import neuronal

class TestsSinapsis(unittest.TestCase):
    def setUp(self):
        self.neurona1 = neuronal.Neurona()
        self.neurona2 = neuronal.Neurona()
        self.sinapsis = self.neurona1.crear_sinapsis_saliente(
          self.neurona2, neuronal.Membrana.umbral
        )

    def tearDown(self):
        self.sinapsis = None
        self.neurona1 = None
        self.neurona2 = None

class TestPesoSinapsis(TestsSinapsis):
    def runTest(self):
        self.neurona1.recibir_estimulo(neuronal.Membrana.umbral)
        self.assertTrue(self.neurona1.esta_activa())
        self.assertFalse(self.neurona2.esta_activa())
        self.neurona1.intentar_disparo()
        self.assertTrue(self.neurona2.esta_activa())
        self.neurona2.intentar_disparo()
        self.assertFalse(self.neurona2.esta_activa())

class TestIgualdad(TestsSinapsis):
    def runTest(self):
        sinap = self.neurona1.crear_sinapsis_saliente(
          self.neurona2
        )
        self.assertEqual(self.sinapsis, sinap)
