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

class TestSecuenciador(unittest.TestCase):
    def setUp(self):
        self.secuenciador = neuronal.Secuenciador()
        self.nucleo = neuronal.Nucleo()
        self.neuroperceptor = neuronal.NeuroPerceptor(3, self.nucleo)
        self.nucleo.crear_neuronas_de_salida(2)
        self.nucleo.crear_neuronas_internas(7)
        self.nucleo.crear_sinapsis_al_azar(12, -10, 10)

    def tearDown(self):
        self.secuenciador = None
        self.nucleo = None

class TestSecuenciado(TestSecuenciador):
    def runTest(self):
        genoma = self.nucleo.obtener_genoma()
        nucleo1 = self.secuenciador.secuenciar(genoma)
        self.assertEqual(genoma, nucleo1.obtener_genoma())
