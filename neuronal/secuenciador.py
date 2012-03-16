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
        # TO-DO, ¿es necesario? No se llama nunca porque secuenciar()
        # ... se encarga de crearlas a la vez que el Nucleo y el
        # ... NeuroPerceptor.
        # TO-DO, No estaría de más un poco de programación defensiva.
        self.nucleo.crear_neuronas_de_entrada(gen[0])
        self.nucleo.crear_neuronas_internas(gen[1])
        self.nucleo.crear_neuronas_de_salida(gen[2])

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
        # TO-DO, no dar por hecho que todo lo que hay a partir del tercer
        # ... gen son "sinapsis". Acotar, por ejemplo, utilizando la
        # ... información del gen0.
        self._crear_sinapsis(genoma[2:])
        return self.nucleo

    def mutar(self, genoma):
        """
        Modifica un gen del genoma.
        """
        # TO-DO, la combinación index() y choice() es rebuscada e
        # ... ineficiente.
        gen = genoma.index(random.choice(genoma))
        exon = genoma[gen].index(random.choice(genoma[gen]))
        # TO-DO, BUG, no tiene en cuenta el gen0.
        # TO-DO, no dar por hecho que todo lo que hay a partir del tercer
        # ... gen son "sinapsis".
        if gen != 1:
            # TO-DO, La amplitud del cambio debería ser configurable.
            amplitud = random.uniform(0.0, 20.0)
            genoma[gen][exon] += random.uniform(-amplitud, amplitud)
        else:
            # Se está modificando el número de neuronas.
            pass

    def mezclar_genomas(self, genomaA, genomaB):
        """
        Dados dos genomas devuelve un núcleo hijo mezclando los genes de
        ambos.
        """
        # TO-DO, 'selector' es innecesario.
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
        # TO-DO, 'tarro' es innecesario.
        tarro = [genomaA[1], genomaB[1]]
        gen1 = []
        for i in xrange(len(genomaA[1])):
            gen1.append(tarro[random.choice(selector)][i])
        # ... y añadir el gen mezclado al genoma.
        genoma.append(gen1)
        # Intercalar, al azar, genes de ambos progenitores en el nuevo
        # ... genoma.
        # TO-DO, 'tarro' es innecesario: se puede hacer el choice sobre
        # ... (genomaA, genomaB), ahorrando de paso la memoria requerida
        # ... por la copia de datos que hace la slice, ya que un xrange()
        # ... en el bucle se puede encargar de delimitar mejor.
        # TO-DO, No dar por hecho que lo que hay a partir del tercer
        # ... gen son sinapsis.
        tarro = [genomaA[2:], genomaB[2:]]
        # TO-DO, No se utiliza el elemento enumerado 'x', por lo tanto
        # ... eliminar la enumeración en favor de un xrange() adecuado.
        for i, x in enumerate(tarro[0]):
            genoma.append(tarro[random.choice(selector)][i])
        #
        # Si procede, mutar el genoma.
        if random.random() <= self.tasa_mutacion:
            self.mutar(genoma)
        # Calculado el juego de genes, devolver el núcleo.
        # TO-DO, devolver el genoma, sino el llamante, que podría querer
        # ... el genoma, tendría que recalcularlo desde el núcleo,
        # ... algo que ya tenemos a mano. El núcleo lo puede coger él
        # ... mismo de .nucleo, o secuenciarlo posteriormente si lo
        # ... desea. Yo incluso diría que mejor no secuenciar aquí, y
        # ... proporcionar un método que haga mezcla y secuenciación
        # ... explícitamente si se desea, por ejemplo
        # ... mezclar_genomas_y_secuenciar(genomaA, genomaB)
        return self.secuenciar(genoma)
