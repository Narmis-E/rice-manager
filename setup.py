from setuptools import setup, find_packages

setup(
  name="rice_manager",
  version="1.1.1",
  description="GTK3 Dotfile Management Tool for Linux Rices",
  author="narmis",
  author_email="narmisecurb@gmail.com",
  url="https://github.com/narmis-e/rice-manager",
  packages=find_packages(),
  include_package_data=True,
  install_requires=[
    "PyGObject",
    "python-dateutil",
    "gobject",
    "pycairo",
    "notify2",
    "pyxdg",
  ],
  entry_points={
    'console_scripts': [
      'rice-manager = rice_manager:main',
    ],
  },
  classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python :: 3",
    "Topic :: Desktop Environment",
    "Topic :: Utilities",
  ],
  license="GPLv3",
)
