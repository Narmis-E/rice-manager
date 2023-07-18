# Rice Manager: Manage and Apply Rices

<p align="center">
  <img width="150" src="rice_manager/data/icons/rice-manager.png">
</p>

Rice Manager is a GTK3 dotfile management tool for Linux rices. It allows you to add, remove, and apply rices on the fly with a straightforward interface.

## What can it do?
You can add and remove dotfiles in the "Add Rice" menu, specify a name for your rice, and then apply or remove added rices in the "View Rice" menu. Rice Manager follows the principles of ricing philosophy, where configuration file for various window managers and applications should be sourced from a single location. Rice Manager is very useful for this reason, as it ensures that configurations can't conflict and eliminates the need for archiving.

![rice-manager-showcase](https://github.com/Narmis-E/rice-manager/assets/109248529/e8284d7f-747f-46d9-bb4d-63db86a54924)
Downloadable from the Releases tab.

## Why Though?
Having created multiple Linux rices myself, I noticed that it is quite an annoying process to manually switch between them. I also wanted an excuse to develop a genuinely useful program, with GTK coming to mind. Initially, I considered creating this as a text-based user interface (TUI) with pure Bash or C++, but I ultimately chose GTK because it looks cool and it works well with Python, which has much nicer operating system parsing and filesystem libraries compared to C++.

## Local Install

Clone the repository:
```
git clone https://github.com/Narmis-E/rice-manager && cd rice-manager
```

Install the package:
```
pip install .
```

Run the program:
```
rice-manager
```

The AppImage was built using:
- [linuxdeploy](https://github.com/linuxdeploy/linuxdeploy)
- [AppImageKit](https://github.com/AppImage/AppImage)

If you encounter any bugs, please create an issue so I can fix it or make a feature request. See the license tab in the about menu for instructions.

### Todo:
- [x] Add a tickbox for removing symlinked rice files on the "View Rice" screen
- [x] Add a GTK_THEME selector to the main menu for quick theme switching
- [ ] Add rices to the main menu
- [ ] Add a duplicate rice button
- [x] Add Flatpak package support or support for other package management systems (pip)
