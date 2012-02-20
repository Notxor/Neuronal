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

from neurona import Neurona

class Capa(object):
    """La capa es un conjunto de neuronas que presenta algunas restricciones.
    Dado el problema que representa la 'cuantización' para simular el
    procesamiento paralelo las restricciones dentro de una capa son las
    siguientes:
        1. Las neuronas que pertenezcan a la misma capa no pueden hacer
           sinapsis entre sí.
        2. Todas las neuronas que pertenezcan a la misma capa deben encontrarse
           en el mismo estado: 'cargando' o 'disparando'."""
    def __init__(self):
        self.neuronas = []

    def add_neurona(self, neurona):
        """Añade una neurona a la capa si cumple con las restricciones."""
        if (self.cumple_condiciones(neurona)):
            neurona.capa = self
            self.neuronas.append(neurona)

    def numero_neuronas(self):
        return len(self.neuronas)

    def cumple_condiciones(self, neurona):
        condiciones = False
        if (isinstance(neurona, Neurona)):
            condiciones = True
        return condiciones
