# -*- coding: utf-8 -*-

#       Copyright (C) 2012 dddddd <dddddd@pyphiverses.org>

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

class TestsNucleo(unittest.TestCase):
    def setUp(self):
        self.nucleo = neuronal.Nucleo()

    def tearDown(self):
        self.nucleo = None

class TestCrearNeurona(TestsNucleo):
    def runTest(self):
        n = self.nucleo.crear_neurona()
        self.assertTrue(isinstance(n, neuronal.Neurona))
        # En la propiedad.
        self.assertEqual(len(self.nucleo.neuronas), 1)
        self.assertEqual(n, self.nucleo.neuronas[0])
        # En la implementación interna.
        self.assertEqual(len(self.nucleo._neuronas), 1)
        self.assertEqual(n, self.nucleo._neuronas[0])

class TestCrearNeuronas(TestsNucleo):
    def runTest(self):
        nn = self.nucleo.crear_neuronas(3)
        self.assertEqual(len(nn), 3)
        self.assertEqual(len(self.nucleo.neuronas), 3)
        self.assertEqual(len(self.nucleo._neuronas), 3)
        # Las neuronas creadas han de ser únicas.
        self.assertTrue(nn[0] != nn[1])
        self.assertTrue(nn[1] != nn[2])
        # En la propiedad.
        self.assertTrue(nn[0] in self.nucleo.neuronas)
        self.assertTrue(nn[1] in self.nucleo.neuronas)
        self.assertTrue(nn[2] in self.nucleo.neuronas)
        # En la implementación interna.
        self.assertTrue(nn[0] in self.nucleo._neuronas)
        self.assertTrue(nn[1] in self.nucleo._neuronas)
        self.assertTrue(nn[2] in self.nucleo._neuronas)

class TestInterconectarNeuronasConNucleo(TestsNucleo):
    def runTest(self):
        vr = -1 * neuronal.Membrana.umbral # Valor de Reset.
        # Las neuronas externas.
        nA = neuronal.Neurona()
        nB = neuronal.Neurona()
        # Sinapsis conectando con nueva neuronas de entrada creada ad-hoc
        s01 = nA.crear_sinapsis_saliente(self.nucleo.crear_neurona(), 1)
        # ... y obtenemos una referencia a la nueva neurona.
        nen1 = s01.neurona_receptora # nen: Neurona Entrada a Nucleo.
        # Método alternativo.
        # ... Creamos la neurona en el núcleo
        nen2 = self.nucleo.crear_neurona()
        # ... y hacemos que sea la receptora otra.
        s02 = nB.crear_sinapsis_saliente(nen2, 2)
        # Estimulan correctamente.
        nA._disparar()
        nB._disparar()
        self.assertEqual(nen1.acumulador, vr + 1)
        self.assertEqual(nen2.acumulador, vr + 2)
        # Se refuerzan en vez de duplicarse.
        s03 = nA.crear_sinapsis_saliente(nen1, -16)
        self.assertTrue(s03 != s02)
        self.assertTrue(s03 == s01)
        self.assertTrue(s03.peso == -15)
        s04 = nA.crear_sinapsis_saliente(nen2, 4) # Ésta es nueva.
        self.assertTrue(s04 != s01)
        self.assertTrue(s04.peso == 4)
        s05 = nB.crear_sinapsis_saliente(nen2, 8)
        self.assertTrue(s05 == s02)
        self.assertTrue(s02.peso == 10)
        # Se estimulan correctamente tras haberlas reforzado/inhibido.
        nA._disparar()
        nB._disparar()
        self.assertEqual(nen1.acumulador, (vr + 1) - 15)
        self.assertEqual(nen2.acumulador, (vr + 2) + 4 + 10)
        # 'vias' tiene referencias a todas las sinapsis.
        self.assertTrue(self.nucleo.vias.has_key((nA, nen1)))
        self.assertTrue(self.nucleo.vias.has_key((nA, nen2)))
        self.assertTrue(self.nucleo.vias.has_key((nB, nen2)))
        self.assertFalse(self.nucleo.vias.has_key((nB, nen1)))

class TestCrearSinapsisAlAzar(TestsNucleo):
    def runTest(self):
        n_entradas = 2 # Número de neuronas entrada.
        n = 20 # Nñumero de neuronas "internas".
        n_salidas = 1 # Número de neuronas salida.
        n_sinapsis = n * 8 # Número de sinapsis entre neuronas del núcleo.
        min_peso_sinapsis = -10
        max_peso_sinapsis = 10
        # Crear el NeuroPerceptor, con sus entradas.
        sentido = neuronal.NeuroPerceptor(n_entradas, self.nucleo)
        # Crear las neuronas internas.
        self.nucleo.crear_neuronas(n)
        self.assertEqual(len(self.nucleo._neuronas), n_entradas + n)
        # Crear las salidas.
        salidas = self.nucleo.crear_neuronas_de_salida(n_salidas)
        self.assertEqual(
          len(self.nucleo._neuronas),
          n_entradas + n + n_salidas
        )
        # Crear las sinapsis aleatoriamente.
        self.nucleo.crear_sinapsis_al_azar(
          n_sinapsis,
          min_peso_sinapsis,
          max_peso_sinapsis
        )
