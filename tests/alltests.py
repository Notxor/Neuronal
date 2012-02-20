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
import sys

sys.path.append('..')

import testneurona
import testsinapsis
import testtablasverdad
import testcapa

class AllTests(unittest.TestSuite):
    def __init__(self):
        # crear la suite
        self.suite = unittest.TestSuite()
        # cargar los tests para la clase Neurona
        self.suite.addTests(unittest.TestLoader().loadTestsFromModule(testneurona))
        # cargar los tests para la clase Sinapsis
        self.suite.addTests(unittest.TestLoader().loadTestsFromModule(testsinapsis))
        # cargar los tests para los operadores logicos comunes
        self.suite.addTest(unittest.TestLoader().loadTestsFromModule(testtablasverdad))
        # cargar los tests para la clase Capa
        self.suite.addTest(unittest.TestLoader().loadTestsFromModule(testcapa))

        self.corredor = unittest.TextTestRunner(verbosity=2)

    def correr(self):
        self.corredor.run(self.suite)

if __name__ == '__main__':
    pruebas = AllTests()
    pruebas.correr()
