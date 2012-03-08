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

class TestsNeuroperceptor(unittest.TestCase):
    def setUp(self):
        self.nucleo = neuronal.Nucleo()

    def tearDown(self):
        self.nucleo = None

class TestCrearNeuroperceptor(TestsNeuroperceptor):
    def runTest(self):
        neuroperceptor = neuronal.NeuroPerceptor(4)
        self.assertTrue(isinstance(neuroperceptor, neuronal.NeuroPerceptor))
        self.assertTrue(neuroperceptor._red is None)
        self.assertEqual(len(neuroperceptor.sensores), 4)

class TestCrearSentidoConectado(TestsNeuroperceptor):
    def runTest(self):
        neuroperceptor = neuronal.NeuroPerceptor(4, self.nucleo)
        self.assertEqual(neuroperceptor._red, self.nucleo)

class TestCrearSentidoMasConectar(TestsNeuroperceptor):
    def runTest(self):
        neuroperceptor = neuronal.NeuroPerceptor(4)
        self.assertTrue(isinstance(neuroperceptor, neuronal.NeuroPerceptor))
        neuroperceptor._conectar_a_red_receptora(self.nucleo)
        self.assertEqual(neuroperceptor._red, self.nucleo)

class TestEnviarSensacion(TestsNeuroperceptor):
    def runTest(self):
        neuroperceptor = neuronal.NeuroPerceptor(3, self.nucleo)
        neuroperceptor.recibir_sensacion_externa((1, 2, 4))
        neuroperceptor.enviar_estimulos()
        # Valor de partida del acumulador en las neuronas.
        a0 = neuronal.Membrana.valor_de_reset
        # Los acumuladores de las neuronas receptoras han reaccionado
        # ... a los estímulos.
        self.assertEqual(
          (a0 + 1, a0 + 2, a0 + 4),
          tuple(self.nucleo._neuronas[i].acumulador for i in xrange(3))
        )