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

# View Rice Window
class ViewRices(Gtk.Window):
  def __init__(self, registry):
    self.registry = registry
    super().__init__(title="Rice Manager")
    self.set_size_request(800, 500)
    self.set_border_width(5)
    hb = configure_header_bar(self)
    #self.set_type_hint(Gdk.WindowTypeHint.DIALOG) # makes the window floating
    self.notebook = Gtk.Notebook()
    self.add(self.notebook)
    self.update_notebook()  # Update the notebook initially

    icon_path = './data/icons/rice-manager.png'
    Gtk.Window.set_default_icon_from_file(icon_path)

    # Create the exit button
    menu_button = Gtk.Button(label="Menu")
    menu_button.set_tooltip_text("Back to the Main Menu")
    menu_button.connect("clicked", self.on_menu_click)
    hb.pack_start(menu_button)

  def on_remove_symlink_clicked(self, checkbox):
    state = checkbox.get_active()
    self.removing_symlinks = state

  def update_notebook(self):
    # Clear the notebook
    num_pages = self.notebook.get_n_pages()
    for _ in range(num_pages):
      self.notebook.remove_page(0)

    directory = os.path.expanduser("~/.local/share/rice-manager/rices")
    if not os.path.exists(directory):
      os.makedirs(directory)

    # Get a list of all JSON files in the directory
    json_files = [f for f in os.listdir(directory) if f.endswith(".json")]

    for json_file in json_files:
      file_path = os.path.join(directory, json_file)
      with open(file_path, "r") as file:
        json_data = json.load(file)
      rice_name = list(json_data.keys())[0]  # Get the rice name from the JSON data

      # Create a new rice page
      rice_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
      label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
      label_box.set_margin_top(10)
      label_box.set_margin_bottom(10)
      label = Gtk.Label(label=rice_name+" 🍚")
      label_box.pack_start(label, False, False, 10)  # Adjust the padding here
      rice_page.pack_start(label_box, False, False, 0)

      # Create and populate a Gtk.TreeView
      list_store = Gtk.ListStore(str, str)
      self.treeview = Gtk.TreeView(model=list_store)
      renderer1 = Gtk.CellRendererText()
      column1 = Gtk.TreeViewColumn("Name", renderer1, text=0)
      self.treeview.append_column(column1)
      renderer2 = Gtk.CellRendererText()
      column2 = Gtk.TreeViewColumn("Path", renderer2, text=1)
      self.treeview.append_column(column2)

      self.treeview.connect("button-press-event", self.on_treeview_double_click)

      scrolled_window = Gtk.ScrolledWindow()
      scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
      rice_page.pack_start(scrolled_window, True, True, 0)
      scrolled_window.add(self.treeview)

      # Iterate over the dotfiles in the rice
      dotfile_data = json_data[rice_name]
      for dotfile in dotfile_data:
        name = dotfile["name"]
        path = dotfile["path"]
        list_store.append([name, path])

      # Create the Apply button
      apply_button = Gtk.Button(label="Apply Rice")
      apply_button.set_tooltip_text("Apply Rice")
      apply_button.set_name("apply-button-name")
      apply_button.connect("clicked", self.on_apply_click, file_path)
      label_box.pack_start(apply_button, False, False, 0)

      # Create the Remove button
      remove_button = Gtk.Button(label="Remove Rice")
      remove_button.set_tooltip_text("Remove Rice")
      remove_button.connect("clicked", self.on_remove_click, file_path, dotfile_data)
      label_box.pack_start(remove_button, False, False, 0)

      remove_symlink= Gtk.CheckButton(label="Remove Symlinks")
      remove_symlink.set_tooltip_text("Unlinks the Rices Symlinks Upon Removal")
      remove_symlink.set_active(True)
      remove_symlink.connect("toggled", self.on_remove_symlink_clicked)
      label_box.pack_start(remove_symlink, False, False, 0)

      # Add the page to the notebook
      self.notebook.append_page(rice_page, Gtk.Label(label=rice_name))

  def on_treeview_double_click(self, treeview, event):
    if event.type == Gdk.EventType.DOUBLE_BUTTON_PRESS and event.button == 1:
      # Perform the desired action on double-click
      selection = treeview.get_selection()
      model, treeiter = selection.get_selected()
      if tree_iter is not None:
        # Get the selected row data and perform the desired action
        path = model[treeiter][1]
        os.system(f"xdg-open {path}")
    # Make sure to propagate the event to other handlers
    return False

  def on_apply_click(self, button, file_path):
    if not os.path.isfile(applied_names):
      with open(applied_names, "w") as file:
        file.write("")
      pass  
    with open(applied_names, "r") as file:
      for line in file:
        os.system(f"unlink ~/.config/{line}")
    with open(applied_names, "w") as paths_file:
      paths_file.write("")
    model = self.treeview.get_model()
    current_page = self.notebook.get_current_page()
    rice_name = self.notebook.get_tab_label_text(self.notebook.get_nth_page(current_page))
    current_rice = os.path.expanduser(f"~/.local/share/rice-manager/rices/{rice_name}.json")
    with open(current_rice, "r") as file:
      data = json.load(file)
    dotfile_data = data[rice_name]
    with open(applied_names, "a") as paths_file:
      for dotfile in dotfile_data:
        dotfile_name = dotfile["name"]
        dotfile_path = dotfile["path"]
        paths_file.write(dotfile_name + "\n")
        os.system(f"ln -sf {dotfile_path} ~/.config/")
        print("["+formatted_datetime+"]", "[INFO]", f" Applied: {dotfile_path}")
    if not os.path.isfile(applied_rice):
      with open(applied_rice, "w") as file:
        file.write(rice_name)
    else:
      with open(applied_rice, "w") as file:
        file.write(rice_name)

    Notify.init("Rice Manager")  # Initialize the Notify module
    notification = Notify.Notification.new(
      f"{rice_name} Rice Applied!",
      "",
    )
    notification.set_urgency(Notify.Urgency.NORMAL)
    notification.set_timeout(2000)  # Set the notification timeout (in milliseconds)
    notification.show()

  def on_remove_click(self, button, file_path, dotfile_data):
    dialog = Gtk.MessageDialog(
      transient_for=self,
      flags=0,
      message_type=Gtk.MessageType.WARNING,
      buttons=Gtk.ButtonsType.YES_NO,
      text="Confirm Removal",
    )
    dialog.format_secondary_text(
      "Are you sure you want to remove the rice and its dotfiles?"
    )
    response = dialog.run()
    dialog.destroy()
    if response == Gtk.ResponseType.YES:
      if getattr(self, 'removing_symlinks', True):
        for dotfile in dotfile_data:
          dotfile_name = dotfile["name"]
          dotfile_path = os.path.expanduser(f"~/.config/{dotfile_name}")
          if os.path.islink(dotfile_path):
            os.unlink(dotfile_path)
            print("["+formatted_datetime+"]", "[INFO]", f" Unlinked: {dotfile_path}")
          # Remove the JSON file
          os.remove(file_path)
          print("["+formatted_datetime+"]", "[INFO]", f" Removed: {file_path}")
          current_page = self.notebook.get_current_page()
          rice_name = self.notebook.get_tab_label_text(self.notebook.get_nth_page(current_page))
          Notify.init("Rice Manager")  # Initialize the Notify module
          notification = Notify.Notification.new(
            f"{rice_name} Rice Removed!",
            "",
          )
          notification.set_urgency(Notify.Urgency.NORMAL)
          notification.set_timeout(2000)  # Set the notification timeout (in milliseconds)
          notification.show()
          with open(applied_rice, "w") as file:
            file.write("")
          with open(applied_names, "w") as file:
            file.write("")
          current_page = self.notebook.get_current_page()
          if current_page >= 0:
              self.notebook.remove_page(current_page)
      else:
          # Remove the JSON file
          os.remove(file_path)
          print("["+formatted_datetime+"]", "[INFO]", f" Removed: {file_path}")
          current_page = self.notebook.get_current_page()
          if current_page >= 0:
            self.notebook.remove_page(current_page)

  def on_menu_click(self, button):
    global last_window_position
    last_window_position = self.get_position()  # Store the current position
    self.update_notebook()
    self.hide()  # Hide the current window
    self.registry['win1'].show_all()  # Show window 1
    if last_window_position:
      self.registry['win1'].move(*last_window_position)  # Set the stored position for win1