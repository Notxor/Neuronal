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
from neurona import Neurona

class Nucleo(Glioblasto):
    def __init__(self,
      cantidad_de_neuronas_internas = 0,
      cantidad_de_neuronas_de_salida = 0
    ):
        Glioblasto.__init__(self)
        self._neuronas = [] # Todas, entradas+internas+salidas.
        self._entradas = []
        self._internas = []
        self._salidas = []
        self.neuroperceptor = None # Se carga al conectarlo.
        # Crear las neuronas internas.
        self.crear_neuronas_internas(cantidad_de_neuronas_internas)
        # Crear las salidas.
        self.crear_neuronas_de_salida(cantidad_de_neuronas_de_salida)

    def _crear_neuronas(self, cantidad):
        """
        Toda neurona que vaya a formar parte de un núcleo ha utilizar
        este método, aunque de forma indirecta, llamando a los métodos
        públicos crear_neuronas*().

        Se le pone una referencia al núcleo en el miembro 'nucleo' de la
        neurona, para detectar si forma parte de un núcleo. Por ejemplo,
        nos interesa saberlo al crear una sinapsis, para actualizar el
        diccionario indexador 'vias' de núcleo.
        """
        # Se crean.
        if cantidad == 0:
            return []
        nn = [Neurona() for i in xrange(cantidad)]
        # Se crea la referencia al núcleo en cada una.
        for n in nn:
            n.nucleo = self
        # Se incluyen.
        self._neuronas.extend(nn)
        return nn

    def crear_neuronas_de_entrada(self, cantidad):
        """
        Crear y devuelve una 'cantidad' de neuronas que actuarán como
        entradas del núcleo.
        """
        nn = self._crear_neuronas(cantidad)
        self._entradas.extend(nn)
        return nn

    def crear_neuronas_internas(self, cantidad):
        """
        Crea y devuelve una 'cantidad' de neuronas (en una lista), que
        formarán parte del núcleo, como neuronas "internas" (las que no
        son ni de entrada ni de salida).
        """
        nn = self._crear_neuronas(cantidad)
        self._internas.extend(nn)
        return nn

    def crear_neuronas_de_salida(self, cantidad):
        """
        Crear y devuelve una 'cantidad' de neuronas que actuarán como
        salidas del núcleo.
        """
        nn = self._crear_neuronas(cantidad)
        self._salidas.extend(nn)
        return nn

    @property
    def neuronas(self):
        """
        Propiedad no necesariamente definitiva para la API, pero aparentemente
        conveniente.
        """
        return self._neuronas

    def estado(self):
        """
        Devuelve una cadena que representa el estado interno del núcleo.
        """
        # Las sinapsis entrantes, de las neuronas de entrada.
        sinapsis_entrantes = []
        aferentes = [e.vias_aferentes for e in self._entradas]
        for via in aferentes:
            sinapsis_entrantes.extend([v for v in via])
        # Se va preparando la salida,
        _s = ''
        sep = ' / ' # Separador.
        # ... Los pesos de las sinapsis de entrada,
        _s = str([s.peso for s in sinapsis_entrantes]) + sep
        # ... y los acumuladores de cada neurona entrada, interna y salida.
        _s += 'E' + str([n.acumulador for n in self._entradas]) + sep
        _s += 'I' + str([n.acumulador for n in self._internas]) + sep
        _s += 'S' + str([n.acumulador for n in self._salidas])
        # Hecho.
        return _s

    def proceso(self, modo = None, veces=1):
        """
        Esto es un buen candidato para ser sustituido por un planificador. El
        caso es que habría que tener mirar la utilización de threads. Pero los
        threads en Python están controlados por el G.I.L. (Global Interpreter
        Lock), cuyo acrónimo no es un diminutivo, que hace que sólo un hilo sea
        ejecutado a la vez... así que no se adelanta mucho.
        """
        if modo is None:
            modo = 'ciclo'
        if modo == 'ciclo':
            """
            Intenta disparos en las neuronas de entrada, las internas y
            la de salida, en ese orden.

            Devuelve una lista con los acumuladores de las salidas justo
            en el momento antes de intentar el disparo.

            Supongo que una 'compreensión de lista' (list comprehension) será
            más rápida que un bucle... siguiendo la programación funcional. Lo
            que hace es recorrer todas las neuronas disparándolas.
            """
            [n.intentar_disparo() for n in self._entradas]
            for i in xrange(veces):
                [n.intentar_disparo() for n in self._internas]
            # OJO, esta forma de obtener los acumuladores de las salidas,
            # ... para conocerlos antes de los reset() de los disparos,
            # ... OBLIGA a que ninguna salida haga sinapsis con ninguna
            # ... otra, ni consigo misma.
            acumuladores_de_salidas = [salida.acumulador
              for salida in self._salidas]
            [n.intentar_disparo() for n in self._salidas]
            return acumuladores_de_salidas
        elif(modo == 'debug'):
            """
            El modo 'debug' aún no hace nada, pero lo que debe hacer es disparar
            una a una las neuronas del núcleo para trazar el funcionamiento de
            la red.
            """
            pass

    def crear_sinapsis_al_azar(self, cantidad, minimo, maximo):
        """
        Crea una 'cantidad' de sinapsis al azar, con un peso entre 'minimo'
        y 'maximo', también al azar. Tanto desde las neuronas de entrada,
        las neuronas internar entre sí y como éstas con las salidas.
        """
        import random
        #n_neuronas = len(self._neuronas)
        posibles_eferentes = tuple(set(self._neuronas) - set(self._salidas))
        for i in xrange(cantidad):
            # Una neurona al azar.
            n1 = random.choice(posibles_eferentes)
            # Otra, que no sea la anterior.
            n2 = random.choice(self._neuronas)
            while n1 == n2 or n2 in self._entradas:
                #print('retry')
                n2 = random.choice(self._neuronas)
            # Un peso al azar.
            peso = float(random.uniform(minimo, maximo))
            #print(peso)
            n1.crear_sinapsis_saliente(n2, peso)

    def obtener_genoma(self):
        """
        Devuelve el 'genoma' del núcleo, convirtiendo todos los valores
        relevantes en una lista de genes.
        """
        genoma = []
        # Primer gen: el número de neuronas de cada tipo.
        genoma.append(
            [len(self._entradas), len(self._internas), len(self._salidas)]
        )
        # Segundo gen: lista de sensibilidades.
        genoma.append(self.neuroperceptor.secuenciar_sensibilidades())
        # Tantos genes como neuronas en el núcleo,
        # ... comienza creando todos los genes con los pesos a cero.
        dimension = len(self._neuronas)
        for n in xrange(dimension):
            genoma.append([0 for i in xrange(dimension)])
        # Recorrer las sinapsis colocando el peso en el sitio correcto.
        for n in self._neuronas:
            for s in n.vias_eferentes:
                # Obtener la fila de la neurona aferente,
                # ... (hay dos genes antes)
                # TO-DO, BUG, dependiente del orden de creación de las
                # ... neuronas. No es fiable.
                fila = genoma[self._neuronas.index(s.neurona_activadora) + 2]
                columna = self._neuronas.index(s.neurona_receptora)
                fila[columna] = s.peso
        return genoma

class SerializadorDot(object):
    def __init__(self):
        pass

    def dump(self, nucleo, f):
        """
        Se guarda el núcleo en formato dot de graphviz.

        Se incluyen dos atributos "privados", sin significado para el
        formato dot, pero que permiten guardar información propia del
        nucleo: __peso de una sinapsis y __acumulador de
        una neurona.
        """
        def _dot_node_def(label, color, acumulador):
            """Declaración de un nodo-neurona"""
            return 'n%s [__acumulador=%s, style=filled, color=%s];\n' % (
              label, acumulador, color)

        def _dot_rel_def(origen, destino, peso):
            """Declaración de una relación-sinapsis."""
            color = 'red' if peso <= 0.0 else 'green'
            _s = 'n%s -> n%s '
            _s += '['
            _s += '__peso=%s, '
            _s += 'label=%s, '
            _s += 'weight=%s, penwidth=%s, '
            _s += 'color=%s]'
            _s += ';\n'
            return _s % (
              origen, destino,
              float(peso),
              int(float(peso)*10)/10.0,
              abs(peso / 100)+1, abs(peso / 100)+1,
              color
            )

        def _sinapsis_salientes(neurona):
            """
            Declaración de todas las sinapsis salientes de una neurona.
            """
            _s = ''
            for si in neurona.vias_eferentes:
                if neurona != si.neurona_activadora:
                    raise "Sinapsis con origen inesperado"
                _s += _dot_rel_def(
                  humano_de[id(neurona)],
                  humano_de[id(si.neurona_receptora)],
                  si.peso
                )
            return _s
        # Los grupos que se van a escribir en el dot.
        # ... (lista, nombre, color).
        clusters = [
          (nucleo._entradas, 'entradas', '"#00dddd"'),
          (nucleo._internas, 'internas', '"#dddddd"'),
          (nucleo._salidas, 'salidas', '"#ffdd22"')
        ]
        humano_de = {} # Traducción por índice a numeración consecutiva.
        # Cabecera del dot, define el gráfico.
        f.write('digraph Neuronal{\n')
        # Subgráficos para cada uno de los grupos de neuronas.
        for neuronas, cluster, color in clusters:
            # Cabecera del grupo/cluster.
            # ... (que el nombre empiece por 'cluster' es relevante).
            f.write('subgraph cluster_%s {\n' % (cluster,))
            for i, n in enumerate(neuronas):
                # Obtener un nuevo nombre para la neurona.
                id_humano = str(cluster[0]) + str(i)
                # Guardar información para traduccir las sinapsis.
                humano_de[id(n)] = id_humano
                # Escribimos la neurona.
                f.write(_dot_node_def(id_humano, color, n.acumulador))
            # Cierre del grupo.
            f.write('}\n')
        # Tras los grupos, escribir las sinapsis.
        for lista_neuronas in [cluster[0] for cluster in clusters]:
            for n in lista_neuronas:
                f.write(_sinapsis_salientes(n))
        # Cierre del dot.
        f.write('}\n')
