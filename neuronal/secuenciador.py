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

from nucleo import Nucleo
import random

class Secuenciador(object):
    '''
    Un secuenciador es capaz de generar un núcleo a partir de su 'genoma' u
    obtener un núcleo hijo a partir del genoma de dos núcleos padre.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.nucleo = None

    def _crear_neuronas(self, gen):
        """
        Crea las neuronas según establecen los datos del primer gen del genoma.
        """
        # TO-DO No estaría de más un poco de programación defensiva.
        self.nucleo.crear_neuronas_de_entrada(gen[0])
        self.nucleo.crear_neuronas_internas(gen[1])
        self.nucleo.crear_neuronas_internas(gen[2])

    def _crear_sinapsis(self, genes):
        """
        Crea las sinapsis del núcleo a partir de la información guardada en
        los genes.
        """
        for i, lista in enumerate(genes):
            for j, peso in enumerate(lista):
                self.nucleo.neuronas[i].crear_sinapsis_saliente(
                                                    self.nucleo.neuronas[j],
                                                    peso
                                                    )

    def secuenciar(self, genoma):
        """
        Genera un nuevo núcleo observando las características que describe el
        parámetro 'genoma'.
        """
        self.nucleo = Nucleo()
        self._crear_neuronas(genoma[0])
        self.nucleo.neuroperceptor.establecer_sensibilidades(genoma[1])
        self._crear_sinapsis(genoma[2:])
        return self.nucleo

    def mezclar_genomas(self, genomaA, genomaB):
        """
        Dados dos genomas devuelve un núcleo hijo mezclando los genes de
        ambos.
        """
        selector = [0, 1]
        genoma = []
        if genomaA[0] != genomaB[0]:
            # El raise es temporal hasta que pensemos en una forma de mezclar
            # genomas con distinto número de neuronas de entrada, salidas e
            # internas.
            raise "Los genomas no son compatibles."
        # Primer gen (en este caso son los dos iguales, si no se ha lanzado una
        # excepción)
        genoma.append(genomaA[0])
        # Mezclar al azar entre todas las sensibilidades.
        tarro = [genomaA[1], genomaB[1]]
        gen1 = [0 for i in len(genomaA[1])]
        for i in len(gen1):
            gen1[i] = tarro[random.choice(selector)][i]
        # Añadir el gen al genoma
        genoma.append(gen1)
        tarro = [genomaA[2:], genomaB[2:]]
        for i in len(tarro[0]):
            genoma.append(tarro[random.choice(selector)][i])

        # Calculado el juego de genes devolver el núcleo
        return self.secuenciar(genoma)
