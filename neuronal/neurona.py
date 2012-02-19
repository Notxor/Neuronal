# -*- coding: utf-8 -*-

#       copyright Notxor 2012

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

from membrana import Membrana
from sinapsis import Sinapsis

class Neurona(object):
    """Elemento estructural base de la red neuronal"""

    def __init__(self):
        """La neurona mantiene una lista de sinapsis llamada 'vias_eferentes' y
        además tiene un valor llamado 'acumulador' donde se va guardando el valor
        de los pesos de las neuronas conectadas. Si llega el momento de disparar
        y la neurona cumple con las condiciones para estar activa, envía un
        mensaje de estimulación a todas las sinapsis registradas como vias
        eferentes."""
        self.vias_eferentes = set()
        self.vias_aferentes = set()
        # Todas, en cualquier sentido.
        # ... Con el índice tuple (activadora, receptora).
        # ... Se carga en self.crear_sinapsis_saliente().
        self.vias = {}
        self._reset()

    def crear_sinapsis_saliente(self, receptora, peso = None):
        """Crea una nueva sinapsis o la refuerza si ya existía."""
        try: # Veamos si existe...
            s = self.vias[(self, receptora)]
        except KeyError: # ... No existía, la creamos y añadimos.
            s = Sinapsis(self, receptora, peso)
            self.vias[(self, receptora)] = s
        else: # ... Sí existía, se refuerza.
            s.reforzar(peso)
        return s

    def recibir_estimulo(self, valor):
        """Actualiza el valor del acumulador. La neurona resulta estar como
        receptora en una sinapsis y la que hace de eferente se ha activado, por
        eso la sinapsis ha mandado un mensaje de actualización del acumulador."""
        self.acumulador += valor

    def esta_activa(self):
        """La neurona está activa si se ha sobrepasado el umbral de la membrana
        y no se ha llegado al valor de bloqueo."""
        return (self.acumulador >= 0 and self.acumulador < Membrana.bloqueo)

    def disparar(self):
        """Si se llama a este miembro y resulta estar activa recorrerá todas las
        vías eferentes para estimularlas. Después de haber disparado realiza una
        puesta a cero."""
        if (self.esta_activa()):
            for s in self.vias_eferentes:
                s.estimular()
        self._reset()

    def _reset(self):
        """Ajusta el acumulador según el valor del umbral de la membrana."""
        self.acumulador = -1 * Membrana.umbral
