# -*- coding: utf-8 -*-

#       Copyright (C) 2012 dddddd <dddddd@pyphiverses.org>
#       Copyright (c) 2012 Notxor <gnotxor@gmail.com>

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

class _Motor(Neurona):
    """Elemento de salida neuromotora."""
    def __init__(self, neuromotor):
        Neurona.__init__(self)
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
        Crea y conecta neuronas de salida en el 'nucleo', tantas como motores
        haya en el neuromotor, mediante sinapsis neurona->motor. Es
        conveniente que dichas neuronas sean las que finalizan la lista de
        neuronas del núcleo. El objetivo es que sean disparadas al final del
        'ciclo' para reducir el número de pasadas que habrá que darle al núcleo.
        """
        n_conexiones = len(self.motoras)
        # Crear neuronas en el destino, que serviran de receptoras.
        red.crear_neuronas(n_conexiones)
        # Conectar los sensores (mediante sinapsis) a las nuevas neuronas.
        for i in xrange(n_conexiones):
            red.neuronas[-i].crear_sinapsis_saliente(self.motoras[i])
        # Guardamos una referencia a la red.
        self._red = red
