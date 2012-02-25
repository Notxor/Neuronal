# -*- coding: utf-8 -*-

# Neuronal - Framework for Neural Networks and Artificial Intelligence
#
# Copyright (C) 2012 dddddd <dddddd@pyphiverses.org>
# Copyright (C) 2012 Notxor <gnotxor@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

import neuronal

class TestsTablasVerdad(unittest.TestCase):
    def setUp(self):
        self.nP = neuronal.Neurona()
        self.nQ = neuronal.Neurona()
        self.nR = neuronal.Neurona()
        self.pr = self.nP.crear_sinapsis_saliente(
          self.nR, neuronal.Membrana.umbral
        )
        self.qr = self.nQ.crear_sinapsis_saliente(
          self.nR, neuronal.Membrana.umbral
        )

    def tearDown(self):
        self.pr = None
        self.qr = None
        self.nP = None
        self.nQ = None
        self.nR = None

class TestAnd(TestsTablasVerdad):
    def runTest(self):
        self.pr.peso = neuronal.Membrana.umbral-1
        self.qr.peso = neuronal.Membrana.umbral-1

        self.nP.recibir_estimulo(neuronal.Membrana.umbral)
        self.nQ.recibir_estimulo(neuronal.Membrana.umbral)
        self.nP.intentar_disparo()
        self.nQ.intentar_disparo()
        self.assertTrue(self.nR.intentar_disparo()) # 1 & 1 -> 1

        self.nP.recibir_estimulo(neuronal.Membrana.umbral)
        self.nQ.recibir_estimulo(0)
        self.nP.intentar_disparo()
        self.nQ.intentar_disparo()
        self.assertFalse(self.nR.intentar_disparo()) # 1 & 0 -> 0

        self.nP.recibir_estimulo(0)
        self.nQ.recibir_estimulo(neuronal.Membrana.umbral)
        self.nP.intentar_disparo()
        self.nQ.intentar_disparo()
        self.assertFalse(self.nR.intentar_disparo()) # 0 & 1 -> 0

        self.nP.recibir_estimulo(0)
        self.nQ.recibir_estimulo(0)
        self.nP.intentar_disparo()
        self.nQ.intentar_disparo()
        self.assertFalse(self.nR.intentar_disparo()) # 0 & 0 -> 0

class TestOr(TestsTablasVerdad):
    def runTest(self):
        self.pr.peso = neuronal.Membrana.umbral
        self.qr.peso = neuronal.Membrana.umbral

        self.nP.recibir_estimulo(neuronal.Membrana.umbral)
        self.nQ.recibir_estimulo(neuronal.Membrana.umbral)
        self.nP.intentar_disparo()
        self.nQ.intentar_disparo()
        self.assertTrue(self.nR.intentar_disparo()) # 1 | 1 -> 1

        self.nP.recibir_estimulo(neuronal.Membrana.umbral)
        self.nQ.recibir_estimulo(0)
        self.nP.intentar_disparo()
        self.nQ.intentar_disparo()
        self.assertTrue(self.nR.intentar_disparo()) # 1 | 0 -> 1

        self.nP.recibir_estimulo(0)
        self.nQ.recibir_estimulo(neuronal.Membrana.umbral)
        self.nP.intentar_disparo()
        self.nQ.intentar_disparo()
        self.assertTrue(self.nR.intentar_disparo()) # 0 | 1 -> 1

        self.nP.recibir_estimulo(0)
        self.nQ.recibir_estimulo(0)
        self.nP.intentar_disparo()
        self.nQ.intentar_disparo()
        self.assertFalse(self.nR.intentar_disparo()) # 0 | 0 -> 0

class TestXOr(TestsTablasVerdad):
    def runTest(self):
        self.pr.peso = neuronal.Membrana.bloqueo-1
        self.qr.peso = neuronal.Membrana.bloqueo-1

        self.nP.recibir_estimulo(neuronal.Membrana.umbral)
        self.nQ.recibir_estimulo(neuronal.Membrana.umbral)
        self.nP.intentar_disparo()
        self.nQ.intentar_disparo()
        self.assertFalse(self.nR.intentar_disparo()) # 1 | 1 -> 0

        self.nP.recibir_estimulo(neuronal.Membrana.umbral)
        self.nQ.recibir_estimulo(0)
        self.nP.intentar_disparo()
        self.nQ.intentar_disparo()
        self.assertTrue(self.nR.intentar_disparo()) # 1 | 0 -> 1

        self.nP.recibir_estimulo(0)
        self.nQ.recibir_estimulo(neuronal.Membrana.umbral)
        self.nP.intentar_disparo()
        self.nQ.intentar_disparo()
        self.assertTrue(self.nR.intentar_disparo()) # 0 | 1 -> 1

        self.nP.recibir_estimulo(0)
        self.nQ.recibir_estimulo(0)
        self.nP.intentar_disparo()
        self.nQ.intentar_disparo()
        self.assertFalse(self.nR.intentar_disparo()) # 0 | 0 -> 0
