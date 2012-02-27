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
        self._entradas = {}
        self._internas = {}
        self._salidas  = {}
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
        self._nucleo.crear_neuronas_de_entrada(len(self._entradas))
        self._nucleo.crear_neuronas_internas(len(self._internas))
        self._nucleo.crear_neuronas_de_salida(len(self._salidas))
        self._ajustar_neuronas()
        self._establecer_sinapsis()
        return self._nucleo

    def _ajustar_neuronas(self):
        keys = self._entradas.keys()
        for i in range(len(keys)):
            self._nucleo._entradas[i].acumulador = self._entradas[keys[i]]
            self._neuronas[keys[i]] = self._nucleo._entradas[i]
        keys = self._internas.keys()
        for i in range(len(keys)):
            self._nucleo._internas[i].acumulador = self._internas[keys[i]]
            self._neuronas[keys[i]] = self._nucleo._internas[i]
        keys = self._salidas.keys()
        for i in range(len(keys)):
            self._nucleo._salidas[i].acumulador = self._salidas[keys[i]]
            self._neuronas[keys[i]] = self._nucleo._salidas[i]

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
            if cargando == 'E' or cargando == 'I' or cargando == 'S':
                self._cargar_info_neurona(tipo=cargando, linea=l)
            elif cargando == 'C':
                self._sinapsis.append(l)

    def _cargar_info_neurona(self, tipo, linea):
        elementos = linea.split(' ')
        if tipo == 'E':
            self._entradas[elementos[0]] = float(elementos[1])
        elif tipo == 'I':
            self._internas[elementos[0]] = float(elementos[1])
        elif tipo == 'S':
            self._salidas[elementos[0]] = float(elementos[1])

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
