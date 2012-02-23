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

class TestsNeuromotor(unittest.TestCase):
    def setUp(self):
        self.nucleo = neuronal.Nucleo()

    def tearDown(self):
        self.nucleo = None

class TestCrearNeuromotor(TestsNeuromotor):
    def runTest(self):
        neuromotor = neuronal.NeuroMotor(4)
        self.assertTrue(isinstance(neuromotor, neuronal.NeuroMotor))
        self.assertTrue(neuromotor._red is None)
        self.assertEqual(len(neuromotor.motoras), 4)

class TestCrearMotorConectado(TestsNeuromotor):
    def runTest(self):
        neuromotor = neuronal.NeuroMotor(4, self.nucleo)
        self.assertEqual(neuromotor._red, self.nucleo)

class TestCrearMotorMasConectar(TestsNeuromotor):
    def runTest(self):
        neuromotor = neuronal.NeuroMotor(4)
        self.assertTrue(isinstance(neuromotor, neuronal.NeuroMotor))
        neuromotor._conectar_a_red_aferente(self.nucleo)
        self.assertEqual(neuromotor._red, self.nucleo)
