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

class Sinapsis(object):
    """Relaciona dos neuronas con un peso. La eferente conecta su salida con la
    receptora. La receptora se estimula con el peso dado."""
    def __init__(self, neurona_activadora, neurona_receptora, peso=0):
        self.neurona_activadora = neurona_activadora
        self.neurona_activadora.vias_eferentes.add(self)
        self.neurona_receptora = neurona_receptora
        self.neurona_receptora.vias_aferentes.add(self)
        self.peso = peso

    def estimular(self):
        """Estimula la neurona receptora."""
        self.neurona_receptora.recibir_estimulo(self.peso)

    def reforzar(self, peso = None):
        if peso is None:
            self.peso += self.peso
        else:
            self.peso += peso

    def __eq__(self, otra):
        """Si las dos neuronas implicadas son las mismas, las sinapsis son iguales."""
        return (self.neurona_activadora == otra.neurona_activadora and
                self.neurona_receptora == otra.neurona_receptora)
