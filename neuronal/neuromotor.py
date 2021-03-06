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

from glioblasto import Glioblasto

class _Motor(Glioblasto):
    """Elemento de salida neuromotora."""
    def __init__(self, neuromotor):
        Glioblasto.__init__(self)
        self.vias_aferentes = set()
        self.neuromotor = neuromotor

class NeuroMotor(object):
    """Conjunto de sensores. Proporciona datos de entrada a una red."""
    def __init__(self, cantidad_de_motores, red = None):
        """
        Las neuronas motoras están en una lista inmutable (tuple), por lo tanto
        no cambian a lo largo de la vida del neuromotor.
        """
        self.motoras = tuple(
          _Motor(self) for i in xrange(cantidad_de_motores)
        )

        self._red = None
        if red is not None:
            self._conectar_a_red_aferente(red)

    def _conectar_a_red_aferente(self, red):
        """
        Crea tantas neuronas de salida en la 'red' como motoras haya en
        este neuromotor, y las conecta (mediante sinapsis salida->motora).

        Es conveniente que dichas neuronas sean las que finalizan la lista de
        neuronas del núcleo. El objetivo es que sean disparadas al final del
        'ciclo' para reducir el número de pasadas que habrá que darle a la
        red. Por lo tanto, lo ideal es llamar a esta función como último
        paso de la creación de la red.
        """
        n_conexiones = len(self.motoras)
        # Crear neuronas en la red, que serviran de emisoras.
        nuevas_salidas = red.crear_neuronas_de_salida(n_conexiones)
        # Conectar las nuevas salidas (mediante sinapsis) a
        # ... las motoras de este neuromotor.
        for i in xrange(n_conexiones):
            nuevas_salidas[i].crear_sinapsis_saliente(self.motoras[i])
        # Guardamos una referencia a la red.
        self._red = red


    def _conectar_motorizacion(self, funciones):
        """
        Este miembro recibe una lista de funciones y le asigna cada una de ellas
        a una neurona motora de la red, de modo que si usa salida es activada
        por la red, se ejecutará el código contenido en la función asociada.
        """
        if (len(funciones) != len(self.motoras)):
            raise "No coincide el número de neuronas con las acciones."
