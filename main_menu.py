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

from utils import *

# Menu Window
class MainMenu(Gtk.Window):
  def __init__(self, registry):
    self.registry = registry
    super().__init__(title="Rice Manager")
    self.set_size_request(800, 500)
    self.set_border_width(5)
    hb = configure_header_bar(self)
    global previous_page_num
    previous_page_num = -1
    themes_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    self.add(themes_box)
    notebook = Gtk.Notebook()
    notebook.set_tab_pos(Gtk.PositionType.LEFT)
    notebook.set_vexpand(False)
    notebook.set_scrollable(True)

    icon_path = './data/icons/rice-manager.png'
    Gtk.Window.set_default_icon_from_file(icon_path)

    add_rice_button = Gtk.Button(label="Add Rice")
    add_rice_button.set_tooltip_text("Add a new Rice")
    add_rice_button.set_name("add-rice-button")
    add_rice_button.connect("clicked", self.on_add_rice_click)
    hb.pack_start(add_rice_button)

    rices_button = Gtk.Button(label="View Rices")
    rices_button.set_tooltip_text("View Your Rices")
    rices_button.connect("clicked", self.on_rices_click)
    hb.pack_start(rices_button)
    themes_box.pack_start(notebook, True, True, 0)

    available_themes = list_gtk_themes()
    current_theme = get_current_theme()
    current_theme_index = None

    for theme in available_themes:
      tab_label = Gtk.Label(label=theme)
      notebook.append_page(Gtk.Box(), tab_label)
      if theme == current_theme:
        current_theme_index = notebook.page_num(notebook.get_nth_page(-1))

    # Add the image and title to the center of every page
    for page_num in range(notebook.get_n_pages()):
      page = notebook.get_nth_page(page_num)
      page_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
      page.add(page_box)

      # Create a grid to hold the image and title
      grid = Gtk.Grid()
      page_box.pack_start(grid, True, True, 0)

      title = Gtk.Label(label="Rice Manager")
      title.override_font(Pango.font_description_from_string(f"{current_font} 17"))
      image = Gtk.Image()
      image.set_from_file('./data/icons/rice-manager-translucent.png')

      # Add the image and title to the grid
      grid.attach(image, 0, 0, 1, 1)
      grid.attach(title, 0, 1, 1, 1)

      # Set the grid properties to center the contents
      grid.set_hexpand(True)
      grid.set_vexpand(True)
      grid.set_halign(Gtk.Align.CENTER)
      grid.set_valign(Gtk.Align.CENTER)

    # Set the current theme page as active using GLib idle function
    if current_theme_index is not None:
      GLib.idle_add(set_current_theme_page, notebook, current_theme_index)
    notebook.connect("switch-page", on_theme_switch)

  def on_add_rice_click(self, button):
    self.registry['win2'].show_all()
    global last_window_position
    last_window_position = self.get_position()  # Store the current position
    self.hide()  # Hide the current window
    self.registry['win2'].set_transient_for(None)  # Unset the transient parent
    self.registry['win2'].show_all()  # Show the new window
    if last_window_position:
      self.registry['win2'].move(*last_window_position)  # Set the stored position for win2

  def on_rices_click(self, button):
    global last_window_position
    last_window_position = self.get_position()  # Store the current position
    self.hide()  # Hide the current window
    self.registry['win3'].set_transient_for(None)  # Unset the transient parent
    self.registry['win3'].show_all()
    if last_window_position:
      self.registry['win3'].move(*last_window_position)  # Set the stored position for win1
    if self.registry['win3'].notebook.get_n_pages() == 0:
      dialog = Gtk.MessageDialog(
        transient_for=self.registry['win3'],  # Set win3 as the transient parent
        flags=0,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text="No Rices Found!",
      )
      dialog.format_secondary_text("Please add a rice")
      dialog.run()
      dialog.destroy()
  apply_css()