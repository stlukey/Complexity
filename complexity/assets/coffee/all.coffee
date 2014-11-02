###
Complexity core coffee script.
###

class Complexity
    constructor: ->
        @showNavbar() unless @gtkApp

    # Simply shows the navbar, used when accessed by other web browsers.
    showNavbar: ->
        $ '.navbar'
            .removeClass 'hidden'

    # Used to check if accessed by gtk app or browser.
    gtkApp:
        navigator.userAgent == "Complexity Gtk"

    @main: -> new Complexity

$ Complexity.main

