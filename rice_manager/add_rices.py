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

from rice_manager.utils import *

# Add Rice Window
class AddRices(Gtk.Window):
  def __init__(self, registry):
    self.registry = registry
    super().__init__(title="Rice Manager")
    self.set_size_request(800, 500)
    self.set_border_width(5)
    hb = configure_header_bar(self)
    #self.set_type_hint(Gdk.WindowTypeHint.DIALOG) # makes the window floating

    # Create a grid to hold the buttons
    grid = Gtk.Grid()
    self.add(grid)
    grid.set_row_spacing(10)
    grid.set_column_spacing(10)

    # Create a box to hold the buttons
    button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    grid.attach(button_box, 0, 0, 1, 1)
    button_box.set_halign(Gtk.Align.CENTER)

    icon_path = os.path.join(package_dir, 'data/icons/rice-manager.png')
    Gtk.Window.set_default_icon_from_file(icon_path)

    # add button
    icon_name = "list-add"
    themed_icon = Gio.ThemedIcon.new(icon_name)
    image = Gtk.Image.new_from_gicon(themed_icon, Gtk.IconSize.BUTTON)
    plus_button = Gtk.Button()
    plus_button.set_name("plus-button")
    plus_button.set_image(image)
    plus_button.connect("clicked", self.on_plus_click)
    button_box.pack_start(
        plus_button, False, False, 0
    )  # Add the "+" button to the button box

    # minus button
    icon_name = "list-remove"
    themed_icon = Gio.ThemedIcon.new(icon_name)
    image = Gtk.Image.new_from_gicon(themed_icon, Gtk.IconSize.BUTTON)
    minus_button = Gtk.Button()
    minus_button.set_name("minus-button")
    minus_button.set_image(image)
    minus_button.connect("clicked", self.on_minus_click)
    button_box.pack_start(
        minus_button, False, False, 0
    )  # Add the "-" button to the button box

    # save button
    save_button = Gtk.Button(label="Save")
    save_button.set_name("save-button")
    save_button.set_tooltip_text("Save Rice")
    save_button.connect("clicked", self.on_save_click)
    button_box.pack_end(
        save_button, False, False, 0
    )  # Add the "-" button to the button box

    # Create the exit button
    menu_button = Gtk.Button(label="Menu")
    menu_button.set_tooltip_text("Back to the Main Menu")
    menu_button.connect("clicked", self.on_menu_click)
    hb.pack_start(menu_button)

    # Create a scrolled window
    scrolled_window = Gtk.ScrolledWindow()
    scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
    grid.attach(scrolled_window, 0, 1, 1, 1)

    # Create the TreeView and ListStore
    self.treeview = Gtk.TreeView()
    scrolled_window.add(self.treeview)
    self.treeview.set_vexpand(True)  # Make the TreeView expand vertically
    self.treeview.set_hexpand(True)  # Make the TreeView expand horizontally

    # Create the columns for the TreeView
    renderer = Gtk.CellRendererText()
    name_column = Gtk.TreeViewColumn("Name", renderer, text=0)
    path_column = Gtk.TreeViewColumn("Path", renderer, text=1)
    self.treeview.append_column(name_column)
    self.treeview.append_column(path_column)
    self.store = Gtk.ListStore(str, str)
    self.treeview.set_model(self.store)

    # Create the rice name entry
    self.entry = Gtk.Entry()
    self.entry.set_placeholder_text("Enter Rice Name")
    self.entry.set_alignment(0.5)
    self.entry.set_max_length(21)
    button_box.pack_end(self.entry, False, False, 0)
    self.entry.connect("button-press-event", self.on_entry_button_press)

  def on_entry_button_press(self, entry, event):
    entry.select_region(0, -1)
    entry.grab_focus()

  def on_plus_click(self, button):
    dialog = Gtk.FileChooserDialog(
      "Select Dotfile Folders",
      None,
      Gtk.FileChooserAction.SELECT_FOLDER,
      (
        Gtk.STOCK_CANCEL,
        Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN,
        Gtk.ResponseType.OK,
      ),
    )
    dialog.set_select_multiple(True)
    dialog.set_current_folder(GLib.get_home_dir())
    dialog.set_local_only(False)  # Show directories from the whole file system
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
      folder_paths = dialog.get_filenames()
      for folder_path in folder_paths:
        print("["+formatted_datetime+"]","[INFO]","Added:", folder_path)
        last_component = os.path.basename(folder_path)
        self.store.append([last_component, folder_path])
    dialog.destroy()

  def on_minus_click(self, button):
    selection = self.treeview.get_selection()
    model, treeiter = selection.get_selected()
    if treeiter is not None:
      path = model.get_value(treeiter, 1)
      self.store.remove(treeiter)
      print("["+formatted_datetime+"]","[INFO]","Removed:", path)

  def on_menu_click(self, button):
    global last_window_position
    last_window_position = self.get_position()  # Store the current position
    self.store.clear()
    self.entry.set_text("")
    self.hide()  # Hide the current window
    self.registry['win1'].show_all()
    if last_window_position:
      self.registry['win1'].move(*last_window_position)  # Set the stored position for win1

  def show_notification(self):
    Notify.init("Rice Manager")  # Initialize the Notify module
    notification = Notify.Notification.new(
      "Rice Saved!",
      "View Your rices by clicking the view rice button in the menu",
    )
    notification.set_urgency(Notify.Urgency.NORMAL)
    notification.set_timeout(2000)  # Set the notification timeout (in milliseconds)
    notification.show()

  def on_save_click(self, button):
    dotfile_data = []
    rice_name = self.entry.get_text()
    if rice_name == "":
      dialog = Gtk.MessageDialog(
        transient_for=self,
        flags=0,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text="No Rice Name Entered",
      )
      dialog.format_secondary_text("Please enter a name for your lovely rice")
      dialog.run()
      dialog.destroy()
    elif len(self.store) == 0:
      dialog = Gtk.MessageDialog(
        transient_for=self,
        flags=0,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text="No Dotfiles Added",
      )
      dialog.format_secondary_text("Please add dotfiles to your lovely rice")
      dialog.run()
      dialog.destroy()
    else:
      for row in self.store:
        name = row[0]
        path = row[1]
        dotfile_entry = {"name": name, "path": path}
        dotfile_data.append(dotfile_entry)
      rice_data = {rice_name: dotfile_data}
      json_data = json.dumps(rice_data, indent=4)

      # Create the directory if it doesn't exist
      rice_directory = os.path.expanduser("~/.local/share/rice-manager/rices/")
      backup_directory = os.path.expanduser("~/.local/share/rice-manager/dotfile-backup/")
      if not os.path.exists(rice_directory):
        os.makedirs(rice_directory)
      if not os.path.exists(backup_directory):
        os.makedirs(backup_directory)

      # Generate the file path with rice_name in the file name
      file_name = f"{rice_name}.json"
      file_path = os.path.join(rice_directory, file_name)

      # Write the JSON data to the file
      with open(file_path, "w") as file:
        file.write(json_data)
      
      for row in self.store:
        name = row[0]
        default = os.path.expanduser(f"~/.config/{name}")
        if os.path.exists(default):
          destination = os.path.join(backup_directory, name)
          os.system(f"cp -r {default} {destination}")

      print("["+formatted_datetime+"]","[INFO]",f"JSON data written to {file_path}")
      self.show_notification()
      self.registry['win3'].update_notebook()
      global last_window_position
      last_window_position = self.get_position()  # Store the current position