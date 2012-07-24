# -*- coding: utf-8 -*-

#    This file is part of emesene.
#
#    emesene is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    emesene is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with emesene; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

''' This module contains the tray icon's class'''

import sys
import PyQt4.QtGui as QtGui

import gui
import extension


class TrayIcon (QtGui.QSystemTrayIcon, gui.BaseTray):
    '''A class that implements the tray icon  of emesene fot Qt4'''
    # pylint: disable=W0612
    NAME = 'TrayIcon'
    DESCRIPTION = 'Qt4 Tray Icon'
    AUTHOR = 'Gabriele "Whisky" Visconti'
    WEBSITE = ''
    # pylint: enable=W0612

    def __init__(self, handler, main_window=None):
        '''
        constructor

        handler -- a e3common.Handler.TrayIconHandler object
        '''
        gui.BaseTray.__init__(self, handler)
        QtGui.QSystemTrayIcon.__init__(self)

        self._handler = handler
        self._main_window = main_window
        self._menu = None
        self._conversations = None
        self._quit_on_close = False

        self.setIcon(QtGui.QIcon(gui.theme.image_theme.logo))
        self.activated.connect(self._on_tray_icon_clicked)

        self.set_login()

        # TODO: this is for mac os, and should be changed in the
        # future (probably no tray icon at all, just the dock icon)
        if sys.platform == 'darwin':
            print 'Here'
            icon = QtGui.QIcon(gui.theme.image_theme.logo)
            qt_app = QtGui.QApplication.instance()
            qt_app.setWindowIcon(icon)
            qt_app.setApplicationName('BHAWH')
        else:
            self.show()

    def _get_quit_on_close(self):
        '''Getter method for property "quit_on_close"'''
        return self._quit_on_close

    def _set_quit_on_close(self, value):
        '''Setter method for property "quit_on_close"'''
        self._quit_on_close = value

    quit_on_close = property(_get_quit_on_close, _set_quit_on_close)

    def set_login(self):    # emesene's
        '''Called when the login window is shown. Sets a proper
        context menu un the Tray Icon.'''
        tray_login_menu_cls = extension.get_default('tray login menu')
        self._menu = tray_login_menu_cls(self._handler)
        self.setIcon(QtGui.QIcon(gui.theme.image_theme.logo))
        if sys.platform == 'darwin':
            QtGui.qt_mac_set_dock_menu(self._menu)
        else:
            self.setContextMenu(self._menu)

    def set_main(self, session):
        '''Called when the main window is shown. Stores the contact list
        and registers the callback for the status_change_succeed event'''
        self._handler.session = session
        self._handler.session.signals.status_change_succeed.subscribe(
                                                    self._on_status_changed)
        tray_main_menu_cls = extension.get_default('tray main menu')
        self._menu = tray_main_menu_cls(self._handler)
        if sys.platform == 'darwin':
            QtGui.qt_mac_set_dock_menu(self._menu)
        else:
            self.setContextMenu(self._menu)

    def set_conversations(self, conversations):     # emesene's
        '''Store a reference to the conversation page'''
        self._conversations = conversations

    # emesene's
    def set_visible(self, visible):
        '''Changes icon's visibility'''
        self.setVisible(visible)

#    def _on_exit_clicked(self, boh):
#        '''Slot called when the user clicks exit in the context menu'''
#        QtGui.QApplication.instance().exit()

    def _on_status_changed(self, status):
        '''This slot is called when the status changes. Update the tray
        icon'''
        self.setIcon(QtGui.QIcon(QtGui.QPixmap(
                                        gui.theme.image_theme.status_icons_panel[status])))


    def _on_tray_icon_clicked(self, reason):
        '''This slot is called when the user clicks the tray icon.
        Toggles main window's visibility'''

        if not self._main_window:
            return

        if reason == QtGui.QSystemTrayIcon.Trigger:
            if not self._main_window.isVisible():
                self._main_window.show()
                self._main_window.activateWindow()
                self._main_window.raise_()
            else: # visible
                if self._main_window.isActiveWindow():
                    self._main_window.hide()
                else:
                    self._main_window.activateWindow()
                    self._main_window.raise_()

        elif reason == QtGui.QSystemTrayIcon.Context:
            if self._menu: # TODO: remove this line
                self._menu.show()



#class TrayIcon (KdeGui.KStatusNotifierItem):
#    '''A class that implements the tray icon of emesene for KDE4'''
#    # pylint: disable=W0612
#    NAME = 'TrayIcon'
#    DESCRIPTION = 'KDE4 Tray Icon'
#    AUTHOR = 'Gabriele Whisky Visconti'
#    WEBSITE = ''
#    # pylint: enable=W0612
#
#    def __init__(self, handler, main_window=None):
#        '''
#        constructor
#
#        handler -- a e3common.Handler.TrayIconHandler object
#        '''
#        KdeGui.KStatusNotifierItem.__init__(self)
#        print ciao_cls
#
#        self._handler = handler
#        self._main_window = main_window
#        self._conversations = None
#
#        self.setStatus(KdeGui.KStatusNotifierItem.Active)
#        self.setIconByPixmap(QtGui.QIcon(
#                             QtGui.QPixmap(
#                             gui.theme.logo).scaled(QtCore.QSize(40, 40))))
#
#        self.activateRequested.connect(self._on_tray_icon_clicked)
#
#
#    def set_login(self):
#        '''does nothing'''
#        pass
#
#    def set_main(self, session):
#        '''does nothing'''
#        self._handler.session = session
#        self._handler.session.signals.status_change_succeed.subscribe(
#                                            self._on_status_changed)
#
#
#    def set_conversations(self, conversations): # emesene's
#        '''Stores a reference to the conversation page'''
#        self._conversations = conversations
#
#
#
#    def _on_status_changed(self, status):
#        self.setIconByPixmap(QtGui.QIcon(QtGui.QPixmap(
#                                        gui.theme.status_icons_panel[status])))
#
#
#    def _on_tray_icon_clicked(self, active, pos):
#        if not self._main_window:
#            return
#
#        if not self._main_window.isVisible():
#            self._main_window.show()
#            self._main_window.activateWindow()
#            self._main_window.raise_()
#        else: # visible
#            if self._main_window.isActiveWindow():
#                self._main_window.hide()
#            else:
#                self._main_window.activateWindow()
#                self._main_window.raise_()





