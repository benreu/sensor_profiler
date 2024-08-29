#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# main.py
# Copyright (C) 2024 programmer <programmer@programmer-System-Product-Name>
# 
# cornell_grape_bud_tester is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# cornell_grape_bud_tester is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk, GLib
import os, sys, glob, serial
import numpy as np

UI_FILE = "src/cornell_grape_bud_tester.ui"


def t_fmt(x, pos): # your custom formatter function: divide by 100.0
	s = '{:.0f}'.format(x / 100.0)
	return s
	
def v_fmt(x, pos): # your custom formatter function: divide by 211.0
	s = '{:.2f}'.format(x / 211.0)
	return s

class GUI:
	def __init__(self):

		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)

		window = self.builder.get_object('window')
		window.show_all()
		
		self.populate_ports()
		self.sensor_array = []
		self.reading_array = []
		self.previous_id = 1

	def populate_ports (self): 
		#ripped off from gnoduino
		menu = self.builder.get_object('menu4')
		for i in menu.get_children():
				menu.remove(i)
		tryports = glob.glob('/dev/ttyS*') + \
					glob.glob('/dev/ttyUSB*') + \
					glob.glob('/dev/ttyACM*')
		menu_item = Gtk.MenuItem.new_with_label("Select port")
		menu_item.set_sensitive(False)
		menu_item.show()
		menu.append( menu_item)
		for i in tryports:
			try:
				s = serial.Serial(i)
				menu_item = Gtk.MenuItem.new_with_label(label = s.portstr)
				menu_item.connect('activate', 
								self.serial_port_menuitem_activated, 
								s.portstr)
				menu_item.show()
				menu.append(menu_item)
				s.close()
			except serial.SerialException:
				pass
				
	def serial_port_menuitem_activated(self, menuitem, port):
		self.com_port = port
		self.builder.get_object('label9').set_label(port)
		self.ser = serial.Serial(self.com_port, 115200)
		self.timeout_id = GLib.timeout_add(10, self.retrieve_serial)
		
	def retrieve_serial (self):
		while self.ser.inWaiting () > 0:
			self.builder.get_object('reading_number').set_label(str(len(self.reading_array)))
			bytes = self.ser.readline()
			text = bytes.decode(encoding="utf-8", errors="strict")
			peltier_id, peltier_value = text.split(" ")
			if peltier_id != self.previous_id:
				self.previous_id = peltier_id
				self.create_new_array()
			self.reading_array.append(int(peltier_value))
		return True

	def create_new_array(self):
		if self.reading_array != []:
			self.sensor_array.append(self.reading_array)
			self.reading_array = []
			self.builder.get_object('sensor_number').set_label(str(len(self.sensor_array)))

	def view_plot_clicked (self, button):
		self.create_new_array()
		window = Gtk.Window()
		box = Gtk.VBox()
		window.add (box)
		from matplotlib.figure import Figure
		from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
		from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar
		figure = Figure(figsize=(4, 4), dpi=100)
		canvas = FigureCanvas(figure)  # a Gtk.DrawingArea
		canvas.set_size_request(900, 600)
		box.pack_start(canvas, True, True, 0)
		toolbar = NavigationToolbar(canvas, window)
		box.pack_start(toolbar, False, False, 0)
		plt = figure.add_subplot(111)
		ax = figure.gca()
		import matplotlib.ticker as tkr     # has classes for tick-locating and -formatting
		time_fmt = tkr.FuncFormatter(t_fmt)    # create your custom formatter function
		volt_fmt = tkr.FuncFormatter(v_fmt)    # create your custom formatter function
		ax.xaxis.set_major_formatter(time_fmt)
		ax.yaxis.set_major_formatter(v_fmt)
		import matplotlib.pyplot as pyplot
		# create colormap
		cm = pyplot.cm.hsv(np.linspace(0, 1, len(self.sensor_array)))
		for index, array in enumerate(self.sensor_array):
			plt.plot(array, label = str(index + 1))
		plt.set_ylabel('Voltage drop')
		plt.set_xlabel('Seconds')
		ax.set_prop_cycle('color', list(cm))
		plt.legend()
		window.show_all()

	def clear_samples_clicked (self, button):
		self.sensor_array = []
		self.reading_array = []
		self.builder.get_object('reading_number').set_label('0')
		self.builder.get_object('sensor_number').set_label(str(len(self.sensor_array) + 1))

	def on_window_destroy(self, window):
		Gtk.main_quit()

def main():
	app = GUI()
	Gtk.main()
		
if __name__ == "__main__":
	sys.exit(main())

