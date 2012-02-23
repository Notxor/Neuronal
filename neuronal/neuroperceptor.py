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

class _Perceptor(Neurona):
    """Elemento de entrada de un neuroperceptor."""
    def __init__(self, neuroperceptor):
        Neurona.__init__(self)
        self.vias_eferentes = set()
        self.neuroperceptor = neuroperceptor

class NeuroPerceptor(object):
    """Conjunto de sensores. Proporciona datos de entrada a una red."""
    def __init__(self, cantidad_de_sensores, red = None):
        """
        Los sensores son una lista inmutable (tuple), por lo tanto no
        cambian a lo largo de la vida del neuroperceptor.
        """
        self.sensores = tuple(
          _Perceptor(self) for i in xrange(cantidad_de_sensores)
        )

        self._red = None
        if red is not None:
            self._conectar_a_red_receptora(red)

    def _conectar_a_red_receptora(self, red):
        """
        Crea y conecta neuronas de entrada en el 'nucleo', tantas como sensores
        haya en el neuroperceptor, mediante sinapsis sensor->neurona. Es
        conveniente que dichas neuronas sean las que inician la lista de
        neuronas del núcleo. El objetivo es que sean disparadas al inicio del
        'ciclo' para reducir el número de pasadas que habrá que darle al núcleo.
        """
        n_conexiones = len(self.sensores)
        # Crear neuronas en el destino, que serviran de receptoras.
        remotas = red.crear_neuronas_de_entrada(n_conexiones)
        # Conectar los sensores (mediante sinapsis) a las nuevas neuronas.
        for i in xrange(n_conexiones):
            self.sensores[i].crear_sinapsis_saliente(remotas[i])
        # Guardamos una referencia a la red.
        self._red = red

    def recibir_sensacion_externa(self, informacion):
        """
        Permite cargar de un golpe los valores en los sensores.
        """
        for i, x in enumerate(informacion):
            for sinapsis in self.sensores[i].vias.values():
                sinapsis.peso = x

    def enviar_estimulos(self):
        """
        Envía todos los estimulos de la sensación actual en este neuroperceptor mediante las sinapsis que están conectadas a la red receptora.
        """
        for sensor in self.sensores:
            for sinapsis in sensor.vias_eferentes:
                sinapsis.estimular()
