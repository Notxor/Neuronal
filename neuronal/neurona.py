# -*- coding: utf-8 -*-

#       copyright (c) Notxor 2012
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

from glioblasto import Glioblasto
from membrana import Membrana

class Neurona(Glioblasto):
    """Elemento base con capacidad de comuncicación de la red neuronal."""
    def __init__(self):
        """Mantiene dos conjuntos de sinapsis, 'vias_eferentes' y
        'vias_aferentes', además de un 'acumulador' donde se va acumulando
        los valores de los estímulos recibidos desde otros elementos
        conectados.

        Es capaz de disparar, si se dan las condiciones adecuadas, lo que
        significa que se envían estímulos por todas las sinapsis registradas
        como vias eferentes.
        """
        Glioblasto.__init__(self)
        self.vias_eferentes = set()
        self.vias_aferentes = set()
        # Un diccionario indexador con todas, en cualquier sentido.
        # ... Se carga en el constructor de Sinapsis.
        # ... Con el índice tuple (activadora, receptora).
        self.vias = {}
        self._reset()
        # Una neurona sólo puede pertenecer a una capa pero también puede actuar
        # de forma independiente como 'sensor' externo
        #self.capa = None

    def recibir_estimulo(self, valor):
        """
        Actualiza acumulador, sumándole 'valor'.

        Es recibido a través de una sinapsis tras haberse activado el
        elemento de la parte emisora, lo que nos define como parte
        receptora. (En concreto, lo ejecuta Sinapsis.estimular()).
        """
        self.acumulador += valor

    def esta_activa(self):
        """
        Está activa si se ha sobrepasado el umbral de la membrana
        y no se ha llegado al valor de bloqueo.
        """
        _acumulador = float(self.acumulador)
        return (_acumulador >= 0 and _acumulador < Membrana.bloqueo)

    def intentar_disparo(self):
        """
        Se dispara si está activa y se resetea en todo caso. Devuelve
        True si se efectuó disparo, False en caso contrario.
        """
        se_disparara = self.esta_activa()
        if se_disparara:
            self._disparar()
        self._reset()
        return se_disparara

    def _disparar(self):
        """Estimula cada una de las vías eferentes."""
        for s in self.vias_eferentes:
            s.estimular()

    def _reset(self):
        """Ajusta el acumulador según el valor del umbral de la membrana."""
        self.acumulador = float(-1 * Membrana.umbral)
