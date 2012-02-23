# -*- coding: utf-8 -*-

#       Copyright (C) 2012 dddddd <dddddd@pyphiverses.org>
#       Copyright (c) 2012 Notxor <gnotxor@gmail.com>

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

class TestsNeuroperceptor(unittest.TestCase):
    def setUp(self):
        self.nucleo = neuronal.Nucleo()

    def tearDown(self):
        self.nucleo = None

class TestCrearSentido(TestsNeuroperceptor):
    def runTest(self):
        neuroperceptor = neuronal.Neuroperceptor(4)
        self.assertTrue(isinstance(neuroperceptor, neuronal.Neuroperceptor))
        self.assertTrue(neuroperceptor._red is None)
        self.assertEqual(len(neuroperceptor.sensores), 4)

class TestCrearSentidoConectado(TestsNeuroperceptor):
    def runTest(self):
        sentido = neuronal.NeuroPerceptor(4, self.nucleo)
        self.assertEqual(sentido._red, self.nucleo)

class TestCrearSentidoMasConectar(TestsNeuroperceptor):
    def runTest(self):
        sentido = neuronal.NeuroPerceptor(4)
        self.assertTrue(isinstance(sentido, neuronal.NeuroPerceptor))
        sentido._conectar_a_red_receptora(self.nucleo)
        self.assertEqual(sentido._red, self.nucleo)

class TestEnviarSensacion(TestsNeuroperceptor):
    def runTest(self):
        sentido = neuronal.NeuroPerceptor(3, self.nucleo)
        sentido.recibir_sensacion_externa((1, 2, 4))
        sentido.enviar_estimulos()
        # Valor de partida del acumulador en las neuronas.
        a0 = float(-1 * neuronal.Membrana.umbral)
        # Los acumuladores de las neuronas receptoras han reaccionado
        # ... a los estímulos.
        self.assertEqual(
          (a0 + 1, a0 + 2, a0 + 4),
          tuple(self.nucleo._neuronas[i].acumulador for i in xrange(3))
        )