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

    def _crear_neuronas(self, gen):
        """
        Crea las neuronas según establece 'gen' (un primer gen de un
        genoma).
        """
        # TO-DO, No estaría de más un poco de programación defensiva.
        self.nucleo.crear_neuronas_de_entrada(gen[0])
        self.nucleo.crear_neuronas_internas(gen[1])
        self.nucleo.crear_neuronas_internas(gen[2])

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
        Genera un nuevo núcleo observando las características que describe
        'genoma'.
        """
        self.nucleo = Nucleo(genoma[0][1], genoma[0][2])
        #
        NeuroPerceptor(genoma[0][0], self.nucleo)
        #
        self.nucleo.neuroperceptor.establecer_sensibilidad(genoma[1])
        self._crear_sinapsis(genoma[2:])
        return self.nucleo

    def mutar(self, genoma):
        """
        Modifica un gen del genoma.
        """
        cromosoma = genoma.index(random.choice(genoma))
        gen = genoma[cromosoma].index(random.choice(genoma[cromosoma]))
        # TO-DO, La amplitud del cambio debería ser configurable.
        if cromosoma != 1:
            amplitud = random.uniform(0.0, 20.0)
            genoma[cromosoma][gen] += random.uniform(-amplitud, amplitud)
        else:
            # Se está modificando el número de neuronas.
            pass

    def mezclar_genomas(self, genomaA, genomaB):
        """
        Dados dos genomas devuelve un núcleo hijo mezclando los genes de
        ambos.
        """
        selector = [0, 1]
        genoma = []
        if genomaA[0] != genomaB[0]:
            # El raise es temporal hasta que pensemos en una forma de
            # ... mezclar genomas con distinto número de neuronas de
            # ... entrada, salida e internas.
            raise "Los genomas no son compatibles."
        # Primer gen (en este caso son los dos iguales, sino se habría
        # ... lanzado una excepción previamente).
        genoma.append(genomaA[0])
        # Mezclar al azar las sensibilidades de cada uno de los genomas,
        tarro = [genomaA[1], genomaB[1]]
        gen1 = [0 for i in genomaA[1]]
        for i in gen1:
            gen1[i] = tarro[random.choice(selector)][i]
        # ... y añadir el gen mezclado al genoma.
        genoma.append(gen1)
        # Intercalar, al azar, genes de ambos progenitores en el nuevo
        # ... genoma.
        tarro = [genomaA[2:], genomaB[2:]]
        for i, x in enumerate(tarro[0]):
            genoma.append(tarro[random.choice(selector)][i])
        #
        # Si procede, mutar el genoma.
        if random.random() <= self.tasa_mutacion:
            self.mutar(genoma)
        # Calculado el juego de genes, devolver el núcleo.
        return self.secuenciar(genoma)
