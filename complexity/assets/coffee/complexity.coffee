##!/usr/bin/env coffee
# -*- coding: UTF-8 -*-
###
    Complexity: all.coffee
    ~~~~~~~~~~~~~~~~~~~~~~
    Core coffee script.

    :copyright: (c) 2014 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
###

class Complexity
    constructor: ->
        @hideNavbar() if @gtkApp

    # Simply hides the navbar, used when accessed by app
    hideNavbar: ->
        $ '.navbar'
            .addClass 'hidden'

    # Used to check if accessed by gtk app or browser.
    gtkApp:
        navigator.userAgent == "Complexity Gtk"

    @main: ->
      new Complexity
      console.log "[Complexity] Core init finished,"

$ Complexity.main

