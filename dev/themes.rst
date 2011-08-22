Creating new theme
==================
Creating a simple new theme is very simple. All one has to do is copy constants.scss from base theme directory amd change the values as per new theme's requirement. New constants.scss should be copied to custom directory.

To make advanced changes, override style definitions as explained in sections below.

Theme structure
===============

::

    fe/src/themes
    |
    |-- <theme-name>
    |   |
    |   |-- css
    |   |    |-- constants.scss  // global variables
    |   |    `-- style.scss      // advanced style definitions
    |   |-- images
    |   `-- manifest


Manifest
========
Create manifest file.
File contains information related to the theme and author.

Example manifest
----------------

::

    name = "Theme Label" # Theme name to show in UI
    author = "Me" # Your name
    website = "http://example.com" # Optional author's URL

Images
======
Put all the images the theme uses in this directory. Image names are case sensitive. Missing images would be taken from base/images directory.

Style
=====
constants.scss:
    provides global variables to be used in all css files.
style.scss:
    Put all css definitions in style.scss you want to override. Refer base styles from base/css/style.scss
