__version__ = "1.1.2"

import os
import json
import warnings
import datetime
import configparser

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Notify", "0.7")
from gi.repository import Gtk, Gdk, Gio, GLib, Pango, Notify, GdkPixbuf
from pathlib import Path

from rice_manager.view_rices import ViewRices
from rice_manager.add_rices import AddRices 
from rice_manager.main_menu import MainMenu

# Create registry
registry = {}

# Create windows 
registry['win1'] = MainMenu(registry)
registry['win2'] = AddRices(registry)
registry['win3'] = ViewRices(registry)

def main():
  win1 = registry['win1']
  win2 = registry['win2'] 
  win3 = registry['win3']

  win1.connect("destroy", Gtk.main_quit)
  win2.connect("destroy", Gtk.main_quit) 
  win3.connect("destroy", Gtk.main_quit)
  
  win1.show_all()
  Gtk.main()

if __name__ == "__main__":
  main()