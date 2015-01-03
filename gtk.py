#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: gtk.py
    ~~~~~~~~~~~~~~~~~~
    
    Gtk interface for Complexity.

    Copyright: (c) 2014 Luke Southam <luke@devthe.com>.
    License: New BSD, see LICENSE for more details.
"""

import os
import sys
from gi.repository import Gtk, Gio, GLib, Gdk
from gi.repository import WebKit

UI_DATA_PATH = '.'

class Handler(object):    
    def __init__(self, app):
        self.app = app
    
    def on_close(self, action):
        print("Clossing..")

    def open_about(self, action):
        about = self.app.about_dialog
        
        about.show()
        about.run()
        about.hide()

    def quit_app(self, *args):
        self.app.quit()

    def new_quiz(self, *args):
        
        self.app.main_window.show_all()

class ComplexityApp(Gtk.Application):
    GLADE_FILE = os.path.join(UI_DATA_PATH, 'gtk.glade')

    def __init__(self, *args, **kwargs):
        super(Gtk.Application, self).__init__(
            application_id="apps.complexity",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )

    def do_activate(self, data=None):
        self.main_window.application = self
        self.main_window.show_all()

        self.add_window(self.main_window)

    def do_startup(self):
        Gtk.Application.do_startup(self)

        builder = Gtk.Builder()

        builder.add_from_file(self.GLADE_FILE)
        try:
            pass
        except:
            print("File Not Found: {}".format(self.GLADE_FILE))
            sys.exit(1)

        self.about_dialog = builder.get_object("AboutDialog")
        self.main_window = builder.get_object("MainWindow")
        self.content_box = builder.get_object("ContentBox")
        self.scroll_window = builder.get_object("ScrollWindow")
        self.status_bar = builder.get_object("StatusBar")

        self.web_view = WebKit.WebView()
        self.web_view.load_uri('http://localhost:5000/')
        self.scroll_window.add(self.web_view)

        settings = WebKit.WebSettings()
        settings.set_property('user-agent', 'Complexity Gtk')
        self.web_view.set_settings(settings)

        self.main_window.show_all()
        builder.connect_signals(Handler(self))

        # self.set_theme()

    def set_theme(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("/usr/share/themes/Adwaita/gtk-3.0/gtk.css")
        
        display = Gdk.Display.get_default()
        screen = display.get_default_screen()

        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, css_provider,
                                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

def complexity_main(callback, *argv):
    app = ComplexityApp()
    exit_code = app.run(argv)
    callback(exit_code)

if __name__ == '__main__':
    complexity_main(exit)

