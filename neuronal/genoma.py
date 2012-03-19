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

class Genoma(object):
    """
    Contiene las instrucciones genéticas de un núcleo.
    """
    def __init__(self, nucleo=None):
        """
        Constructor
        """
        if nucleo == None:
            self.cromosoma_size = [0, 0, 0]
            self.cromosoma_sensibilidad = []
            self.cromosomas_sinapsis = []
