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

class _Perceptor(Glioblasto):
    """Elemento de entrada de un neuroperceptor."""
    def __init__(self, neuroperceptor):
        Glioblasto.__init__(self)
        self.vias_eferentes = set()
        self.neuroperceptor = neuroperceptor

class NeuroPerceptor(object):
    """
    Conjunto de sensores que, conectados a las entradas de una red,
    proporciona estímulos entrantes.

    Atributos:

        sensores
        _red

    Métodos:

      - Para la creación e interconexión:

        __init__(self, cantidad_de_sensores, red = None)
        conectar_a_entradas(self, red, entradas = None)
        crear_neuronas_entrada_y_conectar(self, red)

        Si se utiliza el parámetro 'red' del constructor, las neuronas
        y las conexiones se crearían automáticamente. No enviándolo se
        puede hacer el proceso con los otros dos métodos, usando uno u
        otro dependiendo de si están ya creadas las neuronas o si se
        desean crear en destino.

      - Para manejar la sensación y enviarla:

        recibir_sensacion_externa(self, sensacion)
        enviar_estimulos(self)
    """
    def __init__(self, cantidad_de_sensores, red = None, sensibilidades = None):
        """
        Lo crea con una 'cantidad_de_sensores' (inmutables). Si se pasa
        una 'red', se crearían neuronas de entrada en ella, y se
        conectarían los sensores a ellas mediante sinapsis.
        """
        self.sensores = tuple(
          _Perceptor(self) for i in xrange(cantidad_de_sensores)
        )
        if sensibilidades is None:
            self._sensibilidades = [0 for i in xrange(cantidad_de_sensores)]
        else:
            self._sensibilidades = sensibilidades

        self._red = None
        if red is not None:
            self.crear_neuronas_entrada_y_conectar(red)

    def conectar_a_entradas(self, red, entradas = None):
        """
        Conecta con las 'entradas' de la 'red', permitiendo que los
        estímulos lleguen mediante enviar_estimulos() a las neuronas
        de entrada asociadas.

        Si no se pasa la secuencia de 'entradas', se utilizarían como
        destino la "red._entradas".
        """
        if entradas is None:
            entradas = red._entradas
        # Conectar los sensores (mediante sinapsis) a las nuevas neuronas
        # y añadir el factor de sensibilidad al perceptor
        for i in xrange(len(self.sensores)):
            self.sensores[i].crear_sinapsis_saliente(
                                                     entradas[i],
                                                     self._sensibilidades[i]
                                                     )
        # Se guarda una referencia a la red.
        self._red = red
        # Y una referencia en la red a su neuroperceptor.
        red.neuroperceptor = self

    def crear_neuronas_entrada_y_conectar(self, red):
        """
        Crea neuronas de entrada en la 'red', tantas como sensores haya
        en este neuroperceptor. Mediante sinapsis sensor->neurona el
        neuroperceptor queda conectado a la 'red'.

        Devuelve la secuencia de neuronas recién creadas.
        """
        n_conexiones = len(self.sensores)
        # Crear neuronas en el destino, que servirán de receptoras.
        remotas = red.crear_neuronas_de_entrada(n_conexiones)
        self.conectar_a_entradas(red, remotas)
        return remotas

    def recibir_sensacion_externa(self, sensacion):
        """
        Carga de un golpe la 'sensacion' en los sensores. 'sensacion' es
        una secuencia con tantos elementos como sensores haya en
        el neuroperceptor.
        """
        for i, x in enumerate(sensacion):
            for sinapsis in self.sensores[i].vias.values():
                sinapsis.peso = x

    def enviar_estimulos(self):
        """
        Envía todos los estimulos de la sensación actual, mediante las
        sinapsis existentes sensor->neurona, a la red receptora.
        """
        for sensor in self.sensores:
            for sinapsis in sensor.vias_eferentes:
                sinapsis.estimular()

    def establecer_sensibilidad(self, lista_sensibilidades):
        self._sensibilidades = lista_sensibilidades

    def secuenciar_sensibilidades(self):
        return self._sensibilidades