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
import rice_manager

previous_page_num = -1
current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
warnings.filterwarnings("ignore", category=DeprecationWarning)
last_window_position = None
applied_names = os.path.expanduser("~/.local/share/rice-manager/paths.txt")
applied_rice = os.path.expanduser("~/.local/share/rice-manager/rice.txt")
applied_theme = os.path.expanduser("~/.local/share/rice-manager/theme.txt")
gtk3_settings = os.path.expanduser("~/.config/gtk-3.0/settings.ini")
gtk4_settings = os.path.expanduser("~/.config/gtk-4.0/settings.ini")
package_dir = os.path.dirname(rice_manager.__file__)

def apply_css():
  css_path = os.path.join(package_dir, 'data/css/style.css')
  css_provider = Gtk.CssProvider()
  css_provider.load_from_path(css_path)
  screen = Gdk.Screen.get_default()
  context = Gtk.StyleContext()
  context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

def get_current_rice(self):
  with open(applied_rice, "r") as file:
    current_rice = file.read().strip()
  return current_rice

def set_current_theme_page(notebook, current_theme_index):
  notebook.set_current_page(current_theme_index)

def on_theme_switch(notebook, page, page_num):
  global previous_page_num
  if not os.path.isfile(applied_theme):
    with open(applied_theme, "w") as file:
        file.write("")
    pass
  if previous_page_num != -1 and previous_page_num != page_num:
    current_theme_label = notebook.get_tab_label_text(page)
    settings = Gtk.Settings.get_default()
    if settings.get_property("gtk-theme-name") != current_theme_label:
      config = configparser.ConfigParser()
      config.read(gtk3_settings)
      config.set("Settings", "gtk-theme-name", current_theme_label)
      with open(gtk3_settings, "w") as configfile:
        config.write(configfile)
      settings.set_property("gtk-theme-name", current_theme_label)
      os.system(f"gsettings set org.gnome.desktop.interface gtk-theme '{current_theme_label}'")
      Gio.Settings.sync()
      print("[" + formatted_datetime + "]", "[INFO]", f"GTK Theme Changed to {current_theme_label}")
      Notify.init("Rice Manager")  # Initialize the Notify module
      notification = Notify.Notification.new(
        f"{current_theme_label} Theme Applied!",
        "",
      )
      notification.set_urgency(Notify.Urgency.NORMAL)
      notification.set_timeout(2000)  # Set the notification timeout (in milliseconds)
      notification.show()
      with open(applied_theme, "w") as file:
        file.write(current_theme_label)
  previous_page_num = page_num  # Update previous_page_num with the current page number

def configure_header_bar(self):
  hb = Gtk.HeaderBar()
  hb.set_show_close_button(True)
  hb.props.title = "Rice Manager"
  self.set_titlebar(hb)
  about_button = create_about_button(self)
  hb.pack_end(about_button)
  return hb

def get_current_theme():
  settings = Gtk.Settings.get_default()
  return settings.get_property("gtk-theme-name")

def list_gtk_themes():
  builtin_themes = [
    theme[:-1]
    for theme in Gio.resources_enumerate_children(
        "/org/gtk/libgtk/theme", Gio.ResourceFlags.NONE
    )
  ]

  theme_search_dirs = [
      Path(data_dir) / "themes" for data_dir in GLib.get_system_data_dirs()
  ]
  theme_search_dirs.append(Path(GLib.get_user_data_dir()) / "themes")
  theme_search_dirs.append(Path(GLib.get_home_dir()) / ".themes")
  fs_themes = []

  for theme_search_dir in theme_search_dirs:
    if not theme_search_dir.exists():
      continue
    for theme_dir in theme_search_dir.iterdir():
      if not theme_dir.is_dir():
          continue
      css_files = theme_dir.glob("**/*.css")
      if any(
        "gtk.css" in file.name or "gtk-dark.css" in file.name
        for file in css_files
      ):
        fs_themes.append(theme_dir.name)

  return sorted(set(builtin_themes + fs_themes))

#if __name__ == "__main__":
  #print("Available themes: %s" % ", ".join(list_gtk_themes()))

def on_about_button_clicked(self, button):
  show_about_dialog(self)

def create_about_button(self):
  icon_name = "application-menu"
  themed_icon = Gio.ThemedIcon.new(icon_name)
  image = Gtk.Image.new_from_gicon(themed_icon, Gtk.IconSize.BUTTON)
  about_button = Gtk.Button()
  about_button.set_image(image)
  about_button.connect("clicked", on_about_button_clicked, about_button)
  return about_button

def show_about_dialog(self):
  about_dialog = Gtk.AboutDialog()
  about_dialog.set_transient_for(self.get_toplevel())
  about_dialog.set_modal(True)
  about_dialog.set_program_name("rice-manager")
  about_dialog.set_version("1.1.2")
  about_dialog.set_authors(["narmis"])
  about_dialog.set_copyright("© 2023 narmis")
  license_type = (
    "LICENSED UNDER GPL_3\ninstructions:\nRice Manager is a graphical tool designed to manage dotfiles for your rices.\n"
    +"To add a rice, in the menu hit the 'New Rice' button\nand it will take you to a screen where you can add dotfiles.\n"
    +"To add dotfiles hit the '+' button\nand to remove dotfiles click on a dotfile entry and then hit the '-' button.\n"
    +"After adding a rice, you can either apply or remove it\nby clicking on the 'View Rices' button on the main menu.\n"
    +"Here you can apply or delete rices, or see which dotfiles are present.\n"
    +"Rices are simply saved in a json format and read to display them.\nos commands are then pared for each button:\n"
    +"The Apply button sym links the selected dotfiles to ~/.config\nand the Remove button simply deletes the .json file.\n\n"
    +"If you have any issues with the program or my lack of programming skills,\nplease make an issue here: https://github.com/Narmis-E/rice-manager\n"
    +""
  )
  about_dialog.set_license(license_type)
  about_dialog.set_comments("A GTK3.0 Dotfile Management tool for Linux Rices")
  icon_path = os.path.join(package_dir, 'data/icons/rice-manager.png')
  logo_pixbuf = GdkPixbuf.Pixbuf.new_from_file(icon_path)
  about_dialog.set_default_icon(logo_pixbuf)
  about_dialog.set_logo(logo_pixbuf)  # Set the logo
  response = about_dialog.run()
  if (
      response == Gtk.ResponseType.DELETE_EVENT or response == Gtk.ResponseType.CLOSE
  ):
      about_dialog.destroy()