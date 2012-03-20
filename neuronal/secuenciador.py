# -*- coding: utf-8 -*-

# Neuronal - Framework for Neural Networks and Artificial Intelligence
#
# Copyright (C) 2012 Notxor <gnotxor@gmail.com>
# Copyright (C) 2012 dddddd <dddddd@pyphiverses.org>
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

from nucleo import Nucleo
from neuroperceptor import NeuroPerceptor
from genoma import Genoma
import random

class Secuenciador(object):
    """
    Un secuenciador es capaz de generar un núcleo a partir de un genoma
    u obtener un núcleo hijo a partir del genoma de dos núcleos padre.
    """
    def __init__(self, tasa_mutacion=0.1):
        """
        """
        self.nucleo = None
        self.tasa_mutacion = tasa_mutacion

    def _crear_sinapsis(self, genes):
        """
        Crea las sinapsis del núcleo a partir de la información en
        'genes'.
        """
        for i, lista in enumerate(genes):
            for j, peso in enumerate(lista):
                self.nucleo.neuronas[i].crear_sinapsis_saliente(
                                                    self.nucleo.neuronas[j],
                                                    peso
                                                    )

    def secuenciar(self, genoma):
        """
        Genera un nuevo núcleo observando las características que se
        describen en 'genoma'.
        """
        self.nucleo = Nucleo(
                             genoma.cromosoma_size[1],
                             genoma.cromosoma_size[2]
                             )
        #
        NeuroPerceptor(genoma.cromosoma_size[0], self.nucleo)
        #
        self.nucleo.neuroperceptor.establecer_sensibilidad(
                                                genoma.cromosoma_sensibilidad
                                                          )
        #
        self._crear_sinapsis(genoma.cromosomas_sinapsis)
        return self.nucleo

    def mezclar_genomas(self, genomaA, genomaB):
        """
        Mezcla al azar los genes de los dos genomas dados en un nuevo
        genoma, que se devuelve.
        """
        return genomaA.mezclar(genomaB)

    def mezclar_genomas_y_secuenciar(self, genomaA, genomaB):
        """
        Dados dos genomas devuelve un núcleo secuenciado de la mezcla,
        al azar, de los genes de ambos.
        """
        return self.secuenciar(self.mezclar_genomas(genomaA, genomaB))
