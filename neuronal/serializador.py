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
    Carga y guarda un núcleo en formato propio. El formato es muy simple y
    entendible por humanos.
    """
    def __init__(self, nucleo=None, nombre_fichero=None):
        self._nombre_fichero = nombre_fichero
        self._nucleo = nucleo
        self._lineas = []
        self._neuronas = {}
        self._sinapsis = []

    def cargar(self, nombre_fichero=None):
        """
        Carga la información contenida en nombre_fichero y devuelve un núcleo
        formado a partir de dicha información.
        """
        if nombre_fichero is not None:
            self._nombre_fichero = nombre_fichero
        if self._nucleo is None:
            self._nucleo = Nucleo()
        f = file(self._nombre_fichero, "r")
        self._lineas = f.readlines()
        f.close()
        self._fichero_a_info()
        self._establecer_sinapsis()
        return self._nucleo

    def _establecer_sinapsis(self):
        """
        Crea las sinapsis entre las neuronas del núcleo según la información
        contenida en el fichero.
        """
        for l in self._sinapsis:
            cosas = l.strip().split(' ')
            self._neuronas[cosas[0]].crear_sinapsis_saliente(
                                            self._neuronas[cosas[1]],
                                            float(cosas[2]))

    def _fichero_a_info(self):
        """
        Genera estructuras de datos paralelas con la información del fichero.
        """
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
        """
        Crea una neurona del tipo dado con la información contenida en la linea.
        """
        elementos = linea.split(' ')
        if tipo == 'E':
            neurona = self._nucleo.crear_neuronas_de_entrada(1)
        elif tipo == 'I':
            neurona = self._nucleo.crear_neuronas_internas(1)
        elif tipo == 'S':
            neurona = self._nucleo.crear_neuronas_de_salida(1)
        neurona[0].acumulador = elementos[1]
        self._neuronas[elementos[0]] = neurona[0]

    def guardar(self, nucleo=None):
        """
        Convierte un nucleo dado en un fichero de texto con la estructura del
        mismo.
        """
        # Diccionario que correlaciona entre los id internos de la neuronas
        # ... y los nuevos nombres asignados (más humanos y de numeración
        # ... consecutiva). El índice serán los id y el contenido el
        # ... nuevo nombre. Por lo tanto permite, dado un id, obtener
        # ... rápidamente el nombre que se le asignó. Se utiliza cuando
        # ... se están escribiendo las sinapsis, para enlazar correctamente
        # ... a pesar de la reasignación de nombres. Se carga mientras se
        # ... escriben las neuronas (por grupo).
        neuronombres = {} # Diccionario "traductor".
        # Función para escribir un grupo de neuronas, que se encarga
        # ... también de ir rellenando el dato en el diccionario traductor
        # ... para todas las que va tratando.
        def escribe_grupo(nombre_grupo, lista_neuronas, prefijo):
            # Cabecera de grupo.
            f.write(' ' * 4 + nombre_grupo.capitalize() + ':\n')
            # Cada una de las neuronas de la lista que forma el grupo.
            for i, n in enumerate(lista_neuronas):
                # TO-DO, eliminar limitación de 9999.
                nombre_neurona = prefijo + ('0000' + str(i+1))[-4:]
                f.write(' ' * 8 + nombre_neurona + ' ' +
                        str(float(n.acumulador)) + '\n'
                        )
                # Carga en el diccionario traductor.
                neuronombres[id(n)] = nombre_neurona
        #
        if nucleo is not None:
            self._nucleo = nucleo
        # Si no se dió fichero de salida se usa stdout.
        if self._nombre_fichero is None:
            f = sys.stdout
        else:
            f = file(self._nombre_fichero, "w")
        # Escritura de las neuronas.
        f.write('Neuronas:\n')
        escribe_grupo('entrada', self._nucleo._entradas, 'NE')
        escribe_grupo('internas', self._nucleo._internas, 'NI')
        escribe_grupo('salidas', self._nucleo._salidas, 'NS')
        # Escritura de las sinapsis.
        f.write('Sinapsis:\n')
        for n in self._nucleo.neuronas:
            for s in n.vias_eferentes:
                f.write(' ' * 4 +
                        neuronombres[id(s.neurona_activadora)] + ' ' +
                        neuronombres[id(s.neurona_receptora)] + ' ' +
                        str(float(s.peso)) + '\n')
        # TO-DO, ¿Se puede/debe cerrar stdout?
        f.close()
