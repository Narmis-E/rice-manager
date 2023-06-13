# Rice Manager: Manage and Apply Rices

<p align="center">
  <img width="150" src="myapp.png">
</p>
Rice Manager is a GTK3 dotfile management tool for linux rices. It allows you to add, remove and apply rices on the fly with a straight-forward interface.

## What can it do?
You can add and remove dotfiles in the add rice menu, specify a name for your rice and then apply or remove added rices on the view rice menu. Packaging for flatpak is currently WIP (the FileChooserDialog() for the user's home directory is currently borked), so the only current availability is for AppImages, although I intent to expand and add support for other packge management systems. \
Rice manager abides by the laws of ricing philosophy, where the user's home directory shouldn't be modified and the configuration for various window managers and applications should all be sourced from a singular location. Rice Manager is very useful for this reason, as implementing control over rices ensures that configs can't conflict and they don't need to be archived.

![rice-manager-showcase](https://github.com/Narmis-E/rice-manager/assets/109248529/f56d7f60-c265-4df7-9d11-440493af17da)

## Why Though?
Having created multiple linux rices myself, I noticed that is is quite an annoying process to manually switch between them and I also wanted an excuse to try and develop a actually useful program, with GTK comming to mind.
I originally wanted to create this as a TUI with pure bash or C++, but I decided on GTK because A: it looks cool and B: It works with python which has much nicer os parsing and filesystem libraries built in compared to C++.

## Local Install

Install dependencies:
```
pip3 install PyGObject
```

Clone the repo:
```
git clone https://github.com/Narmis-E/rice-manager && cd rice-manager
```

Run the program
```
python3 rice-manager.py
```

AppImage built using:
https://github.com/linuxdeploy/linuxdeploy
and
https://github.com/AppImage/AppImageKit \

If there are any bugs please make an issue so I can fix it!
(or a request for a feature)

### Todo:
 - [ ] Add tickbox for removing symlinked rice files on view rice screen
 - [ ] Add a GTK_THEME selector to the main menu for quick theme switching
 - [ ] Add CLI arguments for Rice Manager 
 - [ ] Add rices to the main menu
 - [ ] Add a duplicate rice button
 - [ ] Add flatpak package/any other package management system

