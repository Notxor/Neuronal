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
        self._reset()
        # Una neurona sólo puede pertenecer a una capa pero también puede actuar
        # de forma independiente como 'sensor' externo
        #self.capa = None
        # Funciones que serán llamadas tras determinados eventos.
        self.callbacks = {'disparo': [], 'estimulo': []}

    def recibir_estimulo(self, valor):
        """
        Actualiza acumulador, sumándole 'valor'.

        Es recibido a través de una sinapsis tras haberse activado el
        elemento de la parte emisora, lo que nos define como parte
        receptora. (En concreto, lo ejecuta Sinapsis.estimular()).

        Tras aplicar el estímulo se llama a las funciones callback
        registradas en el hook "estimulo". Los datos que recibirán estas
        funciones son: neurona (la que lo ha recibido), valor_previo,
        estimulo (el valor del estímulo recibido) y acumulador (el valor
        del acumulador tras el estímulo). Todos ellos en un diccionario.
        """
        _pre = float(self.acumulador)
        self.acumulador += valor
        _post = float(self.acumulador)
        for callback in self.callbacks['estimulo']:
            callback(
              {
                'neurona': self,
                'valor_previo': _pre,
                'estimulo': valor,
                'acumulador': _post
              }
            )

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
        """
        Estimula cada una de las vías eferentes.

        Tras cada disparo se llama a las funciones callback registradas
        en el hook "disparo". Los datos que recibirán estas funciones
        son: neurona (la neurona disparada). Todos ellos en un
        diccionario.
        """
        for s in self.vias_eferentes:
            s.estimular()
        for callback in self.callbacks['disparo']:
            callback({'neurona': self})

    def _reset(self):
        """Ajusta el acumulador según el valor del umbral de la membrana."""
        self.acumulador = float(-1 * Membrana.umbral)
