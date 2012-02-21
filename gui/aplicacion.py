# -*- coding: utf-8 -*-

#       copyright (c) Notxor 2012

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

import Tkinter as tkinter
import ttk

class Aplicacion(ttk.Frame):
    def say_hi(self):
        print "¡Hola a todos!"

    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.pack()
        self.crear_widgets()

    def crear_widgets(self):
        self.QUIT = ttk.Button(self)
        self.QUIT["text"] = "Salir"
        style = ttk.Style()
        style.configure("Rojo.TButton", foreground="red")

        self.QUIT["command"] =  self.quit
        self.QUIT["style"] = "Rojo.TButton"

        self.QUIT.pack({"side": "left"})

        self.hi_there = ttk.Button(self)
        self.hi_there["text"] = "Hola",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})

raiz = tkinter.Tk()
#raiz.iconbitmap("usb.ico") # En linux no funciona
raiz.title("Prueba con Tkinter")
app = Aplicacion(master=raiz)
app.mainloop()
raiz.destroy()
