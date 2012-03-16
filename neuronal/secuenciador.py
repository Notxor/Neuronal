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
        self.nucleo = Nucleo(genoma[0][1], genoma[0][2])
        #
        NeuroPerceptor(genoma[0][0], self.nucleo)
        #
        self.nucleo.neuroperceptor.establecer_sensibilidad(genoma[1])
        #
        num_neuronas = int(genoma[0][0] + genoma[0][1] + genoma[0][2])
        self._crear_sinapsis(genoma[2:2 + num_neuronas + 1])
        return self.nucleo

    def mutar(self, genoma):
        """
        Modifica un exón de un gen de 'genoma'.
        """
        # Posición de un exón al azar, de un gen al azar.
        i_gen = random.randint(0, len(genoma) - 1)
        j_exon = random.randint(0, len(genoma[i_gen]) - 1)
        # TO-DO, BUG, no tiene en cuenta el gen0.
        # TO-DO, no dar por hecho que todo lo que hay a partir del tercer
        # ... gen son "sinapsis".
        if i_gen != 1:
            # TO-DO, La amplitud del cambio debería ser configurable.
            amplitud = random.uniform(0.0, 20.0)
            genoma[i_gen][j_exon] += random.uniform(-amplitud, amplitud)
        else:
            # Se está modificando el número de neuronas.
            pass

    def mezclar_genomas(self, genomaA, genomaB):
        """
        Mezcla al azar los genes de los dos genomas dados en un nuevo
        genoma, que se devuelve.
        """
        # TO-DO, hay cierta inconsistencia relativa a lo que se considera
        # ... "unidad de mezcla", ya que en unos casos se mezcla
        # ... por exones (las sensibilidades) y en otros por genes. Es
        # ... posible que haya que reorganizar el genoma para evitarlo,
        # ... por ejemplo, haciendo que las sensibilidades sean genes
        # ... propiamente dichos.
        # TO-DO, 'selector' es innecesario.
        selector = [0, 1]
        genoma = []
        if genomaA[0] != genomaB[0]:
            # El raise es temporal hasta que pensemos en una forma de
            # ... mezclar genomas con distinto número de neuronas de
            # ... entrada, salida e internas.
            raise "Los genomas no son compatibles."
        # Primer gen (en este caso son los dos iguales, sino se habría
        # ... lanzado una excepción previamente). El list() asegura que
        # ... se añada una copia, y no una referencia al gen original.
        genoma.append(list(genomaA[0]))
        # Mezclar al azar las sensibilidades de cada uno de los genomas,
        # TO-DO, 'tarro' es innecesario.
        tarro = [genomaA[1], genomaB[1]]
        gen1 = []
        for i in xrange(len(genomaA[1])):
            # El float() asegura que lo que se añade es una copia.
            gen1.append(float(tarro[random.choice(selector)][i]))
        # ... y añadir el gen mezclado al genoma.
        genoma.append(gen1)
        # Intercalar, al azar, genes de ambos progenitores en el nuevo
        # ... genoma.
        # TO-DO, 'tarro' es innecesario: se puede hacer el choice sobre
        # ... (genomaA, genomaB), ahorrando de paso la memoria requerida
        # ... por la copia de datos que hace la slice, ya que un xrange()
        # ... en el bucle se puede encargar de delimitar mejor.
        num_neuronas = int(genomaA[0][0] + genomaA[0][1] + genomaA[0][2])
        tarro = [
          genomaA[2:2 + num_neuronas + 1],
          genomaB[2:2 + num_neuronas + 1]
        ]
        for i in xrange(num_neuronas):
            # No es necesario copiar lo escogido al azar (como en los
            # ... list() ó float() de los casos anteriores) porque las
            # ... slices que componen este tarro ya hacen que sean copias.
            genoma.append(tarro[random.choice(selector)][i])
        #
        # Si procede, mutar el genoma.
        if random.random() < self.tasa_mutacion:
            self.mutar(genoma)
        # Calculado el nuevo genoma, devolverlo.
        return genoma

    def mezclar_genomas_y_secuenciar(self, genomaA, genomaB):
        """
        Dados dos genomas devuelve un núcleo secuenciado de la mezcla,
        al azar, de los genes de ambos.
        """
        return self.secuenciar(self.mezclar_genomas(genomaA, genomaB))
