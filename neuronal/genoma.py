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

#from nucleo import Nucleo
import random

class Genoma(object):
    """
    Contiene las instrucciones genéticas de un núcleo.
    """
    def __init__(self, nucleo=None):
        """
        Constructor. Si se pasa un núcleo como parámetro se rellenan los campos
        con los datos de ese núcleo y se devuelve un objeto 'Genoma', si no, se
        devuelve uno vacío.
        """
        self.cromosoma_size = [0, 0, 0]
        self.cromosoma_sensibilidad = []
        self.cromosomas_sinapsis = []
        if nucleo is not None:
            self.obtener_genoma(nucleo)

    def __eq__(self, otro):
        """
        Comprueba la equivalencia (==) de dos genomas.
        """
        return (self.cromosoma_size == otro.cromosoma_size and
                self.cromosoma_sensibilidad == otro.cromosoma_sensibilidad and
                self.cromosomas_sinapsis == otro.cromosomas_sinapsis)

    def is_compatible(self, otro):
        """
        Devuelve True si dos genomas son compatibles.
        """
        return (self.cromosoma_size == otro.cromosoma_size)

    def obtener_genoma(self, nucleo):
        """
        Establece los valores de los genes que identifican a un núcleo dado.
        """
        # Primer gen: el número de cromosoma_size de cada tipo.
        self.cromosoma_size =  [
                               len(nucleo._entradas),
                               len(nucleo._internas),
                               len(nucleo._salidas)
                               ]
        # Segundo gen: lista de sensibilidades.
        self.cromosoma_sensibilidad = list(
                            nucleo.neuroperceptor.secuenciar_sensibilidades()
                            )
        # Tantos genes como neuronas en el núcleo,
        # ... comienza creando todos los genes con los pesos a cero.
        dimension = len(nucleo._neuronas)
        for n in xrange(dimension):
            self.cromosomas_sinapsis.append([0 for i in xrange(dimension)])
        # Recorrer las sinapsis colocando el peso en el sitio correcto.
        for n in nucleo._neuronas:
            for s in n.vias_eferentes:
                # Obtener la fila de la neurona aferente,
                # ... (hay dos genes antes)
                # TO-DO, BUG, dependiente del orden de creación de las
                # ... neuronas. No es fiable.
                fila = self.cromosomas_sinapsis[
                                nucleo._neuronas.index(s.neurona_activadora)
                                    ]
                columna = nucleo._neuronas.index(s.neurona_receptora)
                fila[columna] = s.peso

    def num_cromosomas(self):
        """
        Devuelve el número de cromosomas del genoma. Ese número es la suma de
        las neuronas, más el gen de tamaño y el de sensibilidad (de ahí el 2).
        """
        return (2 + reduce(lambda x,y: x+y, self.cromosoma_size))

    def mutar(self):
        """
        Modifica al azar el valor de un gen particular. El valor también es
        calculado al azar, dentro de un rango
        """
        i_crom = random.randint(0, self.num_cromosomas())
        if i_crom == 0:
            # TO-DO. No se modifican aún número de neuronas.
            pass
        elif i_crom == 1:
            # Se modifican sensibilidades
            i_gen = random.randint(0, len(self.cromosoma_sensibilidad) - 1)
            amplitud = random.uniform(0.0, 20.0)
            self.cromosoma_sensibilidad[i_gen] += random.uniform(
                                                                 -amplitud,
                                                                  amplitud
                                                                  )
        else:
            # Se modifican sinapsis
            i_crom = int(i_crom - 2)
            cromosoma = self.cromosomas_sinapsis[i_crom]
            i_gen = random.randint(0, len(cromosoma) - 1)
            amplitud = random.uniform(0.0, 20.0)
            cromosoma[i_gen] += random.uniform(-amplitud, amplitud)

    def _mezclar_genomas_compatibles(self, otro):
        """
        Mezcla al azar los genes de dos genomas dados en un nuevo
        genoma. Los tres genomas implicados son compatibles (o de la misma
        familia).
        """
        g = Genoma()
        g.cromosoma_size = self.cromosoma_size
        # Mezclar los genes relativos a la percepción de la red
        g.cromosoma_sensibilidad = []
        for i in xrange(len(self.cromosoma_sensibilidad)):
            g.cromosoma_sensibilidad.append(
                        random.choice([self, otro]).cromosoma_sensibilidad[i]
                        )
        # Mezclar los genes relativos a las sinapsis de la red
        g.cromosomas_sinapsis = []
        for i in xrange(len(self.cromosomas_sinapsis)):
                g.cromosomas_sinapsis.append(
                        random.choice([self, otro]).cromosomas_sinapsis[i]
                        )
        return g

    def mezclar(self, otro):
        """
        Mezcla dos genomas y devuelve uno nuevo.
        """
        if self.is_compatible(otro):
            return self._mezclar_genomas_compatibles(otro)
        else:
            # Esto es temporal hasta que pensemos en una forma de
            # ... mezclar genomas con distinto número de neuronas de
            # ... entrada, salida e internas. De momento devuelve 'None'.
            return None
