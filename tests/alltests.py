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
import sys

sys.path.append('..')

import testneurona
import testsinapsis
import testtablasverdad
import testcapa
import testnucleo
import testneuroperceptor
import testneuromotor
import testsecuenciador
import testgenoma

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
        # cargar los tests para la clase Nucleo
        self.suite.addTest(unittest.TestLoader().loadTestsFromModule(testnucleo))
        # cargar los tests para la clase Neuroperceptor
        self.suite.addTest(unittest.TestLoader().loadTestsFromModule(testneuroperceptor))
        # cargar los tests para la clase Neuromotor
        self.suite.addTest(unittest.TestLoader().loadTestsFromModule(testneuromotor))
        # cargar los tests para la clase Secuenciador
        self.suite.addTest(unittest.TestLoader().loadTestsFromModule(testsecuenciador))
        # cargar los tests para la clase Genoma
        self.suite.addTest(unittest.TestLoader().loadTestsFromModule(testgenoma))

        self.corredor = unittest.TextTestRunner(verbosity=2)

    def correr(self):
        self.corredor.run(self.suite)

if __name__ == '__main__':
    pruebas = AllTests()
    pruebas.correr()
