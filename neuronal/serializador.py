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

import sys
from nucleo import Nucleo

class Serializador(object):
    """
    Carga y guarda un núcleo en formato propio.
    """
    def __init__(self, nucleo=None, nombre_fichero=None):
        self._nombre_fichero = nombre_fichero
        self._nucleo = nucleo
        self._lineas = []
        self._neuronas = {}
        self._sinapsis = []

    def cargar(self, nombre_fichero=None):
        if nombre_fichero != None:
            self._nombre_fichero = nombre_fichero
        if self._nucleo == None:
            self._nucleo = Nucleo()
        f = file(self._nombre_fichero, "r")
        self._lineas = f.readlines()
        f.close()
        self._fichero_a_info()
        self._establecer_sinapsis()
        return self._nucleo

    def _establecer_sinapsis(self):
        for l in self._sinapsis:
            cosas = l.strip().split(' ')
            self._neuronas[cosas[0]].crear_sinapsis_saliente(
                                            self._neuronas[cosas[1]],
                                            float(cosas[2]))

    def _fichero_a_info(self):
        cargando=''
        for l in self._lineas:
            l = l.strip()
            if l.startswith('#') or l == '':
                continue
            if l.startswith('Entradas:'):
                cargando = 'E'
                continue
            elif l.startswith('Internas:'):
                cargando = 'I'
                continue
            elif l.startswith('Salidas:'):
                cargando = 'S'
                continue
            elif l.startswith('Sinapsis:'):
                cargando = 'C'
                continue
            if cargando in ('E', 'I', 'S'):
                self._cargar_info_neurona(tipo=cargando, linea=l)
            elif cargando == 'C':
                self._sinapsis.append(l)

    def _cargar_info_neurona(self, tipo, linea):
        elementos = linea.split(' ')
        if tipo == 'E':
            neurona = self._nucleo.crear_neuronas_de_entrada(1)
        elif tipo == 'I':
            neurona = self._nucleo.crear_neuronas_internas(1)
        elif tipo == 'S':
            neurona = self._nucleo.crear_neuronas_de_salida(1)
        neurona[-1].acumulador = elementos[1]
        self._neuronas[elementos[0]] = neurona[-1]

    def guardar(self, nucleo=None):
        if nucleo != None:
            self._nucleo = nucleo
        if self._nombre_fichero == None:
            f = sys.stdout
        else:
            f = file(self._nombre_fichero, "w")
        # Escritura directa al fichero o a la salida estándar.
        f.write('Neuronas:\n')
        f.write('    Entradas:\n')
        for n in self._nucleo._entradas:
            f.write('        '+str(id(n))+' '+str(n.acumulador)+'\n')
        f.write('    Internas:\n')
        for n in self._nucleo._internas:
            f.write('        '+str(id(n))+' '+str(n.acumulador)+'\n')
        f.write('    Salidas:\n')
        for n in self._nucleo._salidas:
            f.write('        '+str(id(n))+' '+str(n.acumulador)+'\n')
        f.write('Sinapsis:\n')
        for n in self._nucleo.neuronas:
            for s in n.vias_eferentes:
                f.write('    ' + str(id(s.neurona_activadora)) + 
                        ' '    + str(id(s.neurona_receptora)) +
                        ' '    + str(float(s.peso)) + '\n')
        f.close()
