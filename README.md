<div align="center">
  <img src="rice_manager/data/icons/rice-manager.png" alt="Awesome Rices logo" width="150" style="margin-bottom: 30px;">
  <h1 style="font-size: 32px; border: none; line-height: 0; font-weight: bold">Rice Manager</h1>
  <h5 align="center">
    <a href="https://github.com/Narmis-E/rice-manager#traditional-install">Install</a>
    ·
    <a href="https://github.com/Narmis-E/rice-manager#todo">Todo</a>
  </h5>
  <p>A GTK-3 dotfile management tool for Linux rices, allowing you to add, remove, and apply rices on the fly.</p>
    <div style="margin-bottom: 10px">
      <a href="https://github.com/Narmis-E/rice-manager/stargazers">
  		<img alt="Stargazers" src="https://img.shields.io/github/stars/Narmis-E/rice-manager?style=round&logo=starship&color=E5C07A&logoColor=D9E0EE&labelColor=302D41"></a>
    	<a href="https://github.com/Narmis-E/rice-manager/issues">
    	<img alt="Issues" src="https://img.shields.io/github/issues/Narmis-E/rice-manager?style=round&logo=gitbook&color=62AEEF&logoColor=D9E0EE&labelColor=302D41"></a>
    </div>
    <br>
</div>

Rice Manager streamlines the process of managing and switching between dotfile configurations on Linux. It follows the ricing philosophy of maintaining all configs in a central location and linking them together, from one place.

![rice-manager-showcase](https://github.com/Narmis-E/rice-manager/assets/109248529/e8284d7f-747f-46d9-bb4d-63db86a54924)
### With Rice Manager you can:
- Easily add, remove and apply rices
- Give your rices descriptive names
- Seamlessly switch between different rices and themes
- Keep your system configs organized

### Built for Ricing Enthusiasts

As an avid ricer, I found manually managing dotfiles between different configurations to be somewhat tedious and no other tools existed that provided what I was looking for.\
I created Rice Manager as an excuse to build something useful with GTK and Python. The result is a tool tailored to the Linux ricing workflow, making it easy to organize and switch between rices.

# Traditional Install
Downloadable from PyPI:
```
pip install rice-manager
```
or from AppImage in the releases:
```
chmod +x Rice_Manager-x86_64.AppImage
./Rice_Manager-x86_64.AppImage
```

# Local Install

## Pip
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

## AppImage
The AppImage was built using:
- [linuxdeploy](https://github.com/linuxdeploy/linuxdeploy)
- [AppImageKit](https://github.com/AppImage/AppImage)

Clone the AppImage branch:
```
git clone --branch appimage https://github.com/Narmis-E/rice-manager
```
Generate the AppImage:
```
ARCH=x86_64 ./linuxdeploy-x86_64.AppImage --appdir rice-manager/ --output appimage --desktop-file rice-manager/rice-manager.desktop --icon-file rice-manager/myapp.png
```
Make the AppImage executable:
```
ARCH=x86_64 ./appimagetool-x86_64.AppImage rice-manager/
```

If you encounter any bugs, please create an issue so I can fix it or make a feature request. See the license tab in the about menu for instructions.

## Todo:
- [x] Add a tickbox for removing symlinked rice files on the "View Rice" screen
- [x] Add a GTK_THEME selector to the main menu for quick theme switching
- [ ] Add rices to the main menu
- [ ] Add a duplicate rice button
- [x] Add Flatpak package support or support for other package management systems (pip)
