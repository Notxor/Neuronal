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

class Membrana(object):
    """
    Modela simplificadamente una membrana neuronal.

    'umbral' simula el potencial de acción de la membrana neuronal
    y 'bloqueo' indica el punto a partir del cual la membrana pierde su
    conductividad.

    Ambos parámetros son valores estáticos de la clase.

    Proporciona un método de clase 'activa' que permite, dado un
    'potencial' cualquiera en una neurona, saber si la membrana
    estaría activa. Devuelve un booleano.
    """
    umbral = 90.0
    bloqueo = 200.0
    valor_de_reset = float(-1.0 * umbral)
    @classmethod
    def activa(cls, potencial):
        _potencial = float(potencial)
        return (_potencial >= 0.0 and _potencial < cls.bloqueo)
