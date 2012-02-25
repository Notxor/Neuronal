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

from sinapsis import Sinapsis

class Glioblasto(object):
    """Base de todos los elementos de la red neuronal."""
    def __init__(self):
        # Un diccionario indexador con todas las sinapsis, ya sea conectadas
        # ... al elemento o a cualquiera de los que contiene, y sean en el
        # ... sentido (entrada ó salida) que sean.
        # Se carga en el constructor de Sinapsis
        # ... con el índice tuple (activadora, receptora).
        self.vias = {}

    def crear_sinapsis_saliente(self, receptora, peso = None):
        """Crea una nueva sinapsis o la refuerza si ya existía."""
        try: # Veamos si existe...
            s = self.vias[(self, receptora)]
        except KeyError: # ... No existía, la creamos y añadimos.
            s = Sinapsis(self, receptora, peso)
        else: # ... Sí existía, se refuerza.
            s.reforzar(peso)
        return s
