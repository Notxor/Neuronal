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

from glioblasto import Glioblasto
from neurona import Neurona

class Nucleo(Glioblasto):
    def __init__(self,
      cantidad_de_neuronas_internas = 0,
      cantidad_de_neuronas_de_salida = 0
    ):
        Glioblasto.__init__(self)
        self._neuronas = []
        self._entradas = []
        self._salidas = []
        # Crear las neuronas internas.
        self.crear_neuronas(cantidad_de_neuronas_internas)
        # Crear las salidas.
        self.crear_neuronas_de_salida(cantidad_de_neuronas_de_salida)

    def crear_neuronas(self, cantidad):
        """
        Crea y devuelve una 'cantidad' de neuronas (en una lista), que
        formarán parte del núcleo, como neuronas "internas" (las que no
        son ni de entrada ni de salida).

        Toda neurona que vaya a formar parte de un núcleo ha de crearse
        con este método.

        Se le pone una referencia al núcleo en el miembro 'nucleo' de la
        neurona, para detectar si forma parte de un núcleo. Por ejemplo,
        nos interesa saberlo al crear una sinapsis, para actualizar el
        diccionario indexador 'vias' de núcleo.
        """
        # Se crean.
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
        nn = self.crear_neuronas(cantidad)
        self._entradas.extend(nn)
        return nn

    def crear_neuronas_de_salida(self, cantidad):
        """
        Crear y devuelve una 'cantidad' de neuronas que actuarán como
        salidas del núcleo.
        """
        nn = self.crear_neuronas(cantidad)
        self._salidas.extend(nn)
        return nn

    @property
    def neuronas(self):
        """
        Propiedad no necesariamente definitiva para la API, pero aparentemente
        conveniente.
        """
        return self._neuronas

    def proceso(self, modo='ciclo', veces=1):
        """
        Esto es un buen candidato para ser sustituido por un planificador. El
        caso es que habría que tener mirar la utilización de threads. Pero los
        threads en Python están controlados por el G.I.L. (Global Interpreter
        Lock), cuyo acrónimo no es un diminutivo, que hace que sólo un hilo sea
        ejecutado a la vez... así que no se adelanta mucho.
        """
        if (modo == 'ciclo'):
            """
            Supongo que una 'compreensión de lista' (list comprehension) será
            más rápida que un bucle... siguiendo la programación funcional. Lo
            que hace es recorrer todas las neuronas disparándolas.
            """
            [n.intentar_disparo() for n in self._neuronas]
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

    def _dot_file_to_stdout(self):
        def print_sub_arbol(root):
            for s in root.vias_eferentes:
                if root != s.neurona_activadora:
                    print('BUG')
                color = 'red' if s.peso <= 0 else 'green'
                print('n%s -> n%s [weight=%s, penwidth=%s, color=%s];' % (
                  id(root),
                  id(s.neurona_receptora),
                  abs(s.peso / 4), abs(s.peso / 4),
                  color
                  )
                )
        print('digraph G{')
        for i in self._neuronas:
            color = '"#dddddd"'
            if i in self._entradas:
                color = '"#00dddd"'
            elif i in self._salidas:
                color = '"#ffdd22"'
            print('n%s [style=filled, color=%s];' % (id(i), color))
            print_sub_arbol(i)
        print('}')
