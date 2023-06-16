# Rice Manager: Manage and Apply Rices

<p align="center">
  <img width="150" src="myapp.png">
</p>

Rice Manager is a GTK3 dotfile management tool for Linux rices. It allows you to add, remove, and apply rices on the fly with a straightforward interface.

## What can it do?
You can add and remove dotfiles in the "Add Rice" menu, specify a name for your rice, and then apply or remove added rices in the "View Rice" menu. Packaging for Flatpak is currently a work in progress (the `FileChooserDialog()` for the user's home directory is currently not functioning correctly), so the only available option currently is for AppImages. However, there are plans to expand and add support for other package management systems. Rice Manager follows the principles of ricing philosophy, where the user's home directory should not be modified and the configuration for various window managers and applications should be sourced from a single location. Rice Manager is very useful for this reason, as it ensures that configurations can't conflict and eliminates the need for archiving.

![Rice Manager Showcase](https://github.com/Narmis-E/rice-manager/assets/109248529/f56d7f60-c265-4df7-9d11-440493af17da)
Downloadable from the Releases tab.

## Why Though?
Having created multiple Linux rices myself, I noticed that it is quite an annoying process to manually switch between them. I also wanted an excuse to develop a genuinely useful program, with GTK coming to mind. Initially, I considered creating this as a text-based user interface (TUI) with pure Bash or C++, but I ultimately chose GTK because it looks cool and it works well with Python, which has much nicer operating system parsing and filesystem libraries compared to C++.

## Local Install

Install dependencies:
```
pip3 install PyGObject
```

Clone the repository:
```
git clone https://github.com/Narmis-E/rice-manager && cd rice-manager
```

Run the program:
```
python3 rice-manager.py
```

The AppImage was built using:
- [linuxdeploy](https://github.com/linuxdeploy/linuxdeploy)
- [AppImageKit](https://github.com/AppImage/AppImage)

If you encounter any bugs, please create an issue so I can fix it or make a feature request.

### Todo:
- [x] Add a tickbox for removing symlinked rice files on the "View Rice" screen
- [ ] Add a GTK_THEME selector to the main menu for quick theme switching
- [ ] Add command-line arguments for Rice Manager
- [ ] Add rices to the main menu
- [ ] Add a duplicate rice button
- [ ] Add Flatpak package support or support for other package management systems
