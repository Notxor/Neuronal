# -*- coding: utf-8 -*-

#       Copyright (c) 2012 Notxor <gnotxor@gmail.com>
#       Copyright (C) 2012 dddddd <dddddd@pyphiverses.org>

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

from neurona import Neurona

class Nucleo(Neurona):
    def __init__(self):
        Neurona.__init__(self)
        self._neuronas = [] # Notxor intuye que la necesitaremos.

    def crear_neurona(self):
        """
        Crea y devuelve una neurona. Se le pone una referencia al núcleo en el
        miembro 'nucleo' de la neurona, para detectar si forma parte de un
        núcleo. Por ejemplo, nos interesa saberlo al crear una sinapsis, para
        actualizar el diccionario indexador 'vias' de núcleo.

        Toda neurona que vaya a formar parte de un núcleo ha de crearse con
        este método, o su wrapper crear_neuronas(), que permite crear una
        cantidad determinada de neuronas.
        """
        n = Neurona()
        n.nucleo = self
        self._neuronas.append(n)
        return n

    def crear_neuronas(self, cantidad):
        """
        Crea y devuelve una 'cantidad' de neuronas (en una lista), que
        formarán parte del núcleo, de la misma manera que crear_neurona().
        """
        nuevas_neuronas = []
        i = 0
        while i < cantidad:
            nuevas_neuronas.append(self.crear_neurona())
            i += 1
        self._neuronas.extend(nuevas_neuronas)
        return nuevas_neuronas

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
            for i in range(veces):
                [n.intentar_disparo() for n in self._neuronas]
        elif(modo == 'debug'):
            """
            El modo 'debug' aún no hace nada, pero lo que debe hacer es disparar
            una a una las neuronas del núcleo para trazar el funcionamiento de
            la red.
            """
            pass
