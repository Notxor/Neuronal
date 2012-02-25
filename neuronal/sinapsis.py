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

class Sinapsis(object):
    """
    Relaciona dos neuronas con un peso. La activadora conecta su salida con la
    receptora. La receptora se estimula con el peso dado.

    Es política de la librería no instanciar a mano objetos de esta clase.
    Se deben utilizar métodos "fábrica" de otras clases, por ejemplo
    crear_sinapsis_saliente() de Neurona.
    """
    def __init__(self, neurona_activadora, neurona_receptora, peso=0):
        """
        Controla la creación de la nueva sinapsis y se encarga de actualizar
        las estructuras de datos que sirven para enumerar, indexar y buscar
        las sinapsis en las neuronas y los núcleos.

        Para evitar duplicar sinapsis que serían equivalentes, no se deben
        instanciar directamente usando esta clase, sino que se deben usar
        los métodos apropiados de creación de sinapsis, por ejemplo, el
        crear_sinapsis_saliente() de Neurona.
        """
        self.neurona_activadora = neurona_activadora
        self.neurona_activadora.vias_eferentes.add(self)
        self.neurona_receptora = neurona_receptora
        self.neurona_receptora.vias_aferentes.add(self)
        # Ahora actualizamos el diccionario indexador 'vias' de ambas.
        self.neurona_activadora.vias[
          (self.neurona_activadora, self.neurona_receptora)
        ] = self
        self.neurona_receptora.vias[
          (self.neurona_activadora, self.neurona_receptora)
        ] = self
        # Si alguna forma parte de un núcleo, incluimos la sinapsis
        # ... en su diccionario indexador 'vias' también. El atributo
        # ... distintivo 'nucleo' se obtiene en Nucleo.crear_neurona().
        for neu in neurona_activadora, neurona_receptora:
            if hasattr(neu, 'nucleo'):
                neu.nucleo.vias[
                    (self.neurona_activadora, self.neurona_receptora)
                ] = self

        self.peso = peso

    def estimular(self):
        """Estimula la neurona receptora."""
        self.neurona_receptora.recibir_estimulo(self.peso)

    def reforzar(self, peso = None):
        if peso is None:
            self.peso += self.peso
        else:
            self.peso += peso
