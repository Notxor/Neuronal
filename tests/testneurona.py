# -*- coding: utf-8 -*-

#       copyright Notxor 2012

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

class TestsNeurona(unittest.TestCase):
    def setUp(self):
        self.neurona1 = neuronal.Neurona()
        self.neurona2 = neuronal.Neurona()

    def tearDown(self):
        self.neurona1 = None
        self.neurona2 = None

class TestActiva(TestsNeurona):
    def runTest(self):
        self.neurona1.recibir_estimulo(neuronal.Membrana.umbral-1)
        self.assertFalse(self.neurona1.esta_activa())

        self.neurona1.recibir_estimulo(2)
        self.assertTrue(self.neurona1.esta_activa())

class TestReset(TestsNeurona):
    def runTest(self):
        self.neurona1.recibir_estimulo(neuronal.Membrana.umbral)
        self.assertTrue(self.neurona1.esta_activa())
        self.neurona1._reset()
        self.assertFalse(self.neurona1.esta_activa())

class TestConectar(TestsNeurona):
    def runTest(self):
        s = self.neurona1.crear_sinapsis_saliente(self.neurona2)
        self.assertTrue(s in self.neurona1.vias_eferentes)
        self.assertTrue(s not in self.neurona1.vias_aferentes)
        self.assertTrue(self.neurona1.vias.has_key(
          (self.neurona1, self.neurona2))
        )
        self.assertTrue(not self.neurona1.vias.has_key(
          (self.neurona2, self.neurona1))
        )

class TestConectarConPeso(TestsNeurona):
    def runTest(self):
        s = self.neurona1.crear_sinapsis_saliente(self.neurona2, 42)
        self.assertTrue(s.peso == 42)

class TestReforzar(TestsNeurona):
    def runTest(self):
        s = self.neurona1.crear_sinapsis_saliente(self.neurona2, 1)
        self.neurona1.crear_sinapsis_saliente(self.neurona2)
        self.assertTrue(s.peso == 2)
        self.neurona1.crear_sinapsis_saliente(self.neurona2, 7)
        self.assertTrue(s.peso == 9)
