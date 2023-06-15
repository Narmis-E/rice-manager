import os
import json
import warnings
import datetime

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Notify", "0.7")
from gi.repository import Gtk, GLib, Pango, Notify, GdkPixbuf

current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
warnings.filterwarnings("ignore", category=DeprecationWarning)
last_window_position = None

def configure_header_bar(self):
  hb = Gtk.HeaderBar()
  hb.set_show_close_button(True)
  hb.props.title = "Rice Manager"
  self.set_titlebar(hb)
  return hb

def show_about_dialog(self):
  about_dialog = Gtk.AboutDialog()
  about_dialog.set_transient_for(self.get_toplevel())
  about_dialog.set_modal(True)
  about_dialog.set_program_name("rice-manager")
  about_dialog.set_version("1.0.3")
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
  logo_pixbuf = GdkPixbuf.Pixbuf.new_from_file("icons/rice-manager.png")
  about_dialog.set_default_icon(logo_pixbuf)
  about_dialog.set_logo(logo_pixbuf)  # Set the logo
  response = about_dialog.run()
  if (
      response == Gtk.ResponseType.DELETE_EVENT or response == Gtk.ResponseType.CLOSE
  ):
      about_dialog.destroy()

# Menu Window
class MainMenu(Gtk.Window):
  def __init__(self):
    super().__init__(title="Rice Manager")
    self.set_size_request(600, 500)
    self.set_border_width(5)
    hb = configure_header_bar(self)

    # Create a box to hold the buttons and align it to the center
    menu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    align = Gtk.Alignment.new(0.5, 0.5, 0, 0)
    align.add(menu_box)
    self.add(align)

    title = Gtk.Label(label="Rice Manager")
    title.override_font(Pango.font_description_from_string("Sans Serif 17"))
    menu_box.pack_start(title, False, False, 0)

    image = Gtk.Image()
    image.set_from_file("icons/rice-manager-translucent.png")
    menu_box.pack_start(image, False, False, 0)

    icon_path = "icons/rice-manager.png"
    Gtk.Window.set_default_icon_from_file(icon_path)

    add_rice_button = Gtk.Button(label="Add Rice")
    add_rice_button.set_tooltip_text("Add a new 🍚")
    add_rice_button.connect("clicked", self.on_add_rice_click)
    hb.pack_start(add_rice_button)

    rices_button = Gtk.Button(label="View Rices")
    rices_button.set_tooltip_text("View Your 🍚")
    rices_button.connect("clicked", self.on_rices_click)
    hb.pack_start(rices_button)

    about_button = Gtk.Button(label="☰")
    about_button.override_font(Pango.font_description_from_string("Sans Serif 14"))
    about_button.connect("clicked", self.on_about_button_clicked)
    hb.pack_end(about_button)

  def on_about_button_clicked(self, button):
    show_about_dialog(self)

  def on_add_rice_click(self, button):
    global last_window_position
    last_window_position = self.get_position()  # Store the current position
    self.hide()  # Hide the current window
    win2.set_transient_for(None)  # Unset the transient parent
    win2.show_all()  # Show the new window
    if last_window_position:
        win2.move(*last_window_position)  # Set the stored position for win2

  def on_rices_click(self, button):
    global last_window_position
    last_window_position = self.get_position()  # Store the current position
    self.hide()  # Hide the current window
    win3.set_transient_for(None)  # Unset the transient parent
    win3.show_all()  # Show window 1
    if last_window_position:
      win3.move(*last_window_position)  # Set the stored position for win1
    if win3.notebook.get_n_pages() == 0:
      dialog = Gtk.MessageDialog(
          transient_for=win3,  # Set win3 as the transient parent
          flags=0,
          message_type=Gtk.MessageType.INFO,
          buttons=Gtk.ButtonsType.OK,
          text="No 🍚 Found!",
      )
      dialog.format_secondary_text("Please add a rice")
      dialog.run()
      dialog.destroy()

# Add Rice Window
class AddRices(Gtk.Window):
  def __init__(self):
    super().__init__(title="Rice Manager")
    self.set_size_request(600, 500)
    self.set_border_width(5)
    hb = configure_header_bar(self)

    # Create a grid to hold the buttons
    grid = Gtk.Grid()
    self.add(grid)
    grid.set_row_spacing(10)
    grid.set_column_spacing(10)

    # Create a box to hold the buttons
    button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    grid.attach(button_box, 0, 0, 1, 1)

    icon_path = "icons/rice-manager.png"
    Gtk.Window.set_default_icon_from_file(icon_path)

    # add button
    plus_button = Gtk.Button(label="+")
    plus_button.set_tooltip_text("Add a Dotfile Folder")
    plus_button.override_font(Pango.font_description_from_string("Sans Serif 18"))
    plus_button.connect("clicked", self.on_plus_click)
    button_box.pack_start(
        plus_button, False, False, 0
    )  # Add the "+" button to the button box

    # minus button
    minus_button = Gtk.Button(label="-")
    minus_button.set_tooltip_text("Remove Selected Dotfile Folder")
    minus_button.override_font(Pango.font_description_from_string("Sans Serif 18"))
    minus_button.connect("clicked", self.on_minus_click)
    button_box.pack_start(
        minus_button, False, False, 0
    )  # Add the "-" button to the button box

    # save button
    save_button = Gtk.Button(label="Save")
    save_button.set_tooltip_text("Remove Selected Dotfile Folder")
    save_button.connect("clicked", self.on_save_click)
    button_box.pack_end(
        save_button, False, False, 0
    )  # Add the "-" button to the button box

    # Create the exit button
    menu_button = Gtk.Button(label="Menu")
    menu_button.set_tooltip_text("Back to the Main Menu")
    menu_button.connect("clicked", self.on_menu_click)
    hb.pack_start(menu_button)

    about_button = Gtk.Button(label="☰")
    about_button.override_font(Pango.font_description_from_string("Sans Serif 14"))
    about_button.connect("clicked", self.on_about_button_clicked)
    hb.pack_end(about_button)

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

  def on_about_button_clicked(self, button):
    show_about_dialog(self)

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
    win1.show_all()  # Show window 1
    if last_window_position:
      win1.move(*last_window_position)  # Set the stored position for win1

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
      dialog.format_secondary_text("Please enter a name for your lovely 🍚")
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
      dialog.format_secondary_text("Please add dotfiles to your lovely 🍚")
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
      directory = os.path.expanduser("~/.local/share/rice-manager/rices/")
      if not os.path.exists(directory):
          os.makedirs(directory)

      # Generate the file path with rice_name in the file name
      file_name = f"{rice_name}.json"
      file_path = os.path.join(directory, file_name)

      # Write the JSON data to the file
      with open(file_path, "w") as file:
          file.write(json_data)

      print("["+formatted_datetime+"]","[INFO]",f"JSON data written to {file_path}")
      self.show_notification()
      win3.update_notebook()
      global last_window_position
      last_window_position = self.get_position()  # Store the current position

# View Rice Window
class ViewRices(Gtk.Window):
  def __init__(self):
    super().__init__(title="Rice Manager")
    self.set_size_request(600, 500)
    self.set_border_width(5)
    hb = configure_header_bar(self)
    self.notebook = Gtk.Notebook()
    self.add(self.notebook)
    self.update_notebook()  # Update the notebook initially

    icon_path = "icons/rice-manager.png"
    Gtk.Window.set_default_icon_from_file(icon_path)

    # Create the exit button
    menu_button = Gtk.Button(label="Menu")
    menu_button.set_tooltip_text("Back to the Main Menu")
    menu_button.connect("clicked", self.on_menu_click)
    hb.pack_start(menu_button)

    about_button = Gtk.Button(label="☰")
    about_button.override_font(Pango.font_description_from_string("Sans Serif 14"))
    about_button.connect("clicked", self.on_about_button_clicked)
    hb.pack_end(about_button)

  def on_remove_symlink_clicked(self, checkbox):
    state = checkbox.get_active()
    self.removing_symlinks = state

  def on_about_button_clicked(self, button):
    show_about_dialog(self)
      
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
      apply_button.connect("clicked", self.on_apply_click, file_path)
      label_box.pack_start(apply_button, False, False, 0)

      # Create the Remove button
      remove_button = Gtk.Button(label="Remove Rice")
      remove_button.connect("clicked", self.on_remove_click, file_path, dotfile_data)
      label_box.pack_start(remove_button, False, False, 0)

      remove_symlink= Gtk.CheckButton(label="Remove Symlinks")
      remove_symlink.set_active(True)
      remove_symlink.connect("toggled", self.on_remove_symlink_clicked)
      label_box.pack_start(remove_symlink, False, False, 0)

      # Add the page to the notebook
      self.notebook.append_page(rice_page, Gtk.Label(label=rice_name))

  def on_apply_click(self, button, file_path):
    model = self.treeview.get_model()
    for row in model:
      dotfile_path = row[1]
      os.system(f"ln -sf {dotfile_path} ~/.config/")
      print("["+formatted_datetime+"]", "[INFO]", f"🍚 Applied: {file_path}")

    dialog = Gtk.MessageDialog(
      transient_for=self,
      flags=0,
      message_type=Gtk.MessageType.INFO,
      buttons=Gtk.ButtonsType.OK,
      text="Rice Applied",
    )
    dialog.format_secondary_text("All dotfiles have been applied.")
    dialog.run()
    dialog.destroy()

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
                    print("["+formatted_datetime+"]", "[INFO]", f"🍚 Unlinked: {dotfile_path}")
            # Remove the JSON file
            os.remove(file_path)
            print("["+formatted_datetime+"]", "[INFO]", f"🍚 Removed: {file_path}")
            current_page = self.notebook.get_current_page()
            if current_page >= 0:
                self.notebook.remove_page(current_page)
        else:
            # Remove the JSON file
            os.remove(file_path)
            print("["+formatted_datetime+"]", "[INFO]", f"🍚 Removed: {file_path}")
            current_page = self.notebook.get_current_page()
            if current_page >= 0:
                self.notebook.remove_page(current_page)

  def on_menu_click(self, button):
    global last_window_position
    last_window_position = self.get_position()  # Store the current position
    self.update_notebook()
    self.hide()  # Hide the current window
    win1.show_all()  # Show window 1
    if last_window_position:
      win1.move(*last_window_position)  # Set the stored position for win1

win1 = MainMenu()
win2 = AddRices()
win3 = ViewRices()
win1.connect("destroy", Gtk.main_quit)
win2.connect("destroy", Gtk.main_quit)
win3.connect("destroy", Gtk.main_quit)
win1.show_all()
Gtk.main()