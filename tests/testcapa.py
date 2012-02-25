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

class TestsCapa(unittest.TestCase):
    def setUp(self):
        self.capa = neuronal.Capa()
        self.neurona1 = neuronal.Neurona()
        self.neurona2 = neuronal.Neurona()
        self.capa.add_neurona(self.neurona1)
        self.capa.add_neurona(self.neurona2)

    def tearDown(self):
        self.neurona1 = None
        self.neurona2 = None
        self.capa = None

class TestSize(TestsCapa):
    def runTest(self):
        self.assertEqual(self.capa.numero_neuronas(), 2)

# XXX hay que comprobar que dos neuronas en la misma capa no están conectadas
class TestCondiciones(TestsCapa):
    def runTest(self):
        valor = 0       # nu puede cumplir condiciones: es un entero
        self.assertFalse(self.capa.cumple_condiciones(valor))