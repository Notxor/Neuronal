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

class TestGenoma(unittest.TestCase):
    def setUp(self):
        self.nucleo = neuronal.Nucleo()
        neuronal.NeuroPerceptor(3, self.nucleo)
        self.nucleo.crear_neuronas_de_salida(2)
        self.nucleo.crear_neuronas_internas(7)
        self.nucleo.crear_sinapsis_al_azar(12, -10, 10)
        self.genoma = neuronal.Genoma(self.nucleo)

    def tearDown(self):
        self.genoma = None
        self.nucleo = None

class TestMezclado(TestGenoma):
    def runTest(self):
        secuenciador = neuronal.Secuenciador()
        nucleo1 = secuenciador.secuenciar(self.genoma)
        nucleo1.crear_sinapsis_al_azar(10, -15, 10)
        genoma1 = nucleo1.obtener_genoma()
        self.assertNotEqual(self.genoma, genoma1)
        genoma2 = secuenciador.mezclar_genomas(genoma1, self.genoma)
        self.assertNotEqual(self.genoma, genoma2)
        self.assertNotEqual(genoma1, genoma2)
        genoma3 = secuenciador.mezclar_genomas(genoma1, self.genoma)
        self.assertNotEqual(genoma2, genoma3)

class TestMutar(TestGenoma):
    def runTest(self):
        genoma1 = self.genoma.mutar()
        self.assertNotEqual(self.genoma, genoma1)
