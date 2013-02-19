#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module adds a menu item to the nautilus right-click menu which allows to run the selected file via optirun just through the right-clicking"""

#   nautilus-optirun.py version 3.0
#
#   Copyright 2009-2011 Giuseppe Penone <giuspen@gmail.com>
#   Copyright 2012 Modified by Melroy van den Berg <webmaster1989@gmail.com>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#   MA 02110-1301, USA.

from gi.repository import Nautilus, GObject, Gtk, GdkPixbuf
import urllib, subprocess, re
import locale, gettext
import os

APP_NAME = "NautilusOptirun"
LOCALE_PATH = "/usr/share/locale/"
ICONPATH = "/usr/share/pixmaps/NautilusOptirun.svg"
# internationalization
locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(APP_NAME, LOCALE_PATH)
gettext.textdomain(APP_NAME)
_ = gettext.gettext
# post internationalization code starts here

class NautilusOptirun(GObject.GObject, Nautilus.MenuProvider):
    """Implements the 'Nautilus Optirun' extension to the nautilus right-click menu"""

    def __init__(self):
        """Nautilus crashes if a plugin doesn't implement the __init__ method"""
        try:
            factory = Gtk.IconFactory()
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(ICONPATH)
            iconset = Gtk.IconSet.new_from_pixbuf(pixbuf)
            factory.add("preferences-nautilus-optirun", iconset)
            factory.add_default()
        except: pass

    def run(self, menu, source_path):
        """Runs the Adding of selected file via optirun"""
        executable = os.system("grep 'Exec=' " + source_path + " |sed s/Exec=// ")
        print executable
        bash_string = "optirun %s &" % executable	
        subprocess.call(bash_string, shell=True)

    def get_file_items(self, window, sel_items):
        """Adds the 'Nautilus Optirun' menu item to the Nautilus right-click menu,
           connects its 'activate' signal to the 'run' method passing the list of selected file"""
        if len(sel_items) != 1 or sel_items[0].is_directory() or sel_items[0].get_uri_scheme() != 'file':
            return
        uri_raw = sel_items[0].get_uri()
        if len(uri_raw) < 7: return
        source_path = urllib.unquote(uri_raw[7:])
        filetype = subprocess.Popen("file -i %s" % re.escape(source_path), shell=True, stdout=subprocess.PIPE).communicate()[0]
	print filetype

        if "application" or "text" in filetype:
            item = Nautilus.MenuItem(name='NautilusPython::preferences-nautilus-optirun',
                                     label=_('Run via Optirun'),
                                     tip=_('Run the selected file on discrete video card'),
                                     icon='preferences-nautilus-optirun')
            item.connect('activate', self.run, source_path)
            return item,
