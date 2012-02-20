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

class Glioblasto(object):
    """Base de todos los elementos de la red neuronal."""
    def __init__(self):
        # Un diccionario indexador con todas las sinapsis, ya sea conectadas
        # ... al elemento o a cualquiera de los que contiene, y sean en el
        # ... sentido (entrada ó salida) que sean.
        # Se carga en el constructor de Sinapsis
        # ... con el índice tuple (activadora, receptora).
        self.vias = {}
