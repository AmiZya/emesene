# -*- coding: utf-8 -*-

'''This module contains classes to represent the conversation page.'''

import logging

import PyQt4.QtGui      as QtGui

import gui
import extension

log = logging.getLogger('qt4ui.ConversationPage')

class ConversationPage (gui.base.ConversationManager, QtGui.QTabWidget):
    '''The Conversation Page'''
    # pylint: disable=W0612
    NAME = 'MainPage'
    DESCRIPTION = 'The widget used to to display the conversation screen'
    AUTHOR = 'Gabriele "Whisky" Visconti'
    WEBSITE = ''
    # pylint: enable=W0612

    def __init__(self, session, on_last_close, parent):
        '''Constructor'''
        gui.base.ConversationManager.__init__(self, session, on_last_close)
        QtGui.QTabWidget.__init__(self, parent)

        self.setTabsClosable(True)
        self.setDocumentMode(True)

        # to prevent top level window's destruction:
        self.qt_parent = parent

        self.tabCloseRequested.connect(self._on_tab_close_request)
        # this was sbuscribed in base class' constructor. Now it's not
        self.session.signals.contact_attr_changed.subscribe(
                                    self._on_contact_attr_changed)


    def __del__(self):
        log.debug('conversation manager adieeeeeeeuuuu ;______;')

    def get_parent(self): # emesene's
        '''Return a reference to the top level window containing this page'''
        return QtGui.QTabWidget.parent(self).parent()

    def set_current_page(self, tab_index): # emesene's
        '''Show the chat tab at the given index'''
        QtGui.QTabWidget.setCurrentIndex(self, tab_index)

    #[START] -------------------- GUI.BASE.CONVERSATIONMANAGER_OVERRIDE

    def add_new_conversation(self, session, conv_id, members):
        '''Creates a new chat tab and returns it. This implements base's
        class abstract method.'''
        conversation_cls = extension.get_default('conversation')
        conversation = conversation_cls(session, conv_id, members)
        account = session.contacts.get(members[0])
        conversation.tab_index = self.addTab(conversation,
                    (unicode(account.display_name)))
        conversation.conv_manager = self
        return conversation

    def get_dimensions(self):
        '''
        Returns a tuple containing width, height, x coordinate, y coordinate
        '''
        size = self.size()
        position = self.pos()
        return size.width(), size.height(), position.x(), position.y()

    def hide_all(self):
        '''Hides the window'''
        # FIXME: shouldn't this be called on something else??
        self.get_parent().hide()

    def is_active(self):
        '''return True if the conversation manager is active'''
        return self.get_parent().hasFocus()

    def is_maximized(self):
        return self.get_parent().isMaximized()

    def present(self, conversation, b_single_window=False):
        '''Raises the tab containing the given conversation'''
        self.setCurrentIndex(conversation.tab_index)

    def remove_conversation(self, conversation):
        '''Removes the chat tab. This implements base's class
        abstract method.'''
        index = self.indexOf(conversation)
        self.removeTab(index)

    def set_message_waiting(self, conversation, is_waiting): # emesene's
        '''Not Sure what to do here....'''
        log.info('Conversation: %s; is_waiting: %s' %
                 (conversation, is_waiting))

    def _on_contact_attr_changed(self, account, change_type, old_value,
            do_notify=True):
        '''called when an attribute of a contact changes.
        Overridden to update tabs'''
        # it's not subscribed in base class anymore, so don't invoke this
        #gui.base.ConversationManager._on_contact_attr_changed(self, account,
        #                                                      change_type,
        #                                                      old_value,
        #                                                      do_notify)
        for conversation in self.conversations.values():
            if account in conversation.members:
                index = self.indexOf(conversation)
                account = self.session.contacts.get(conversation.members[0])
                icon = QtGui.QIcon(gui.theme.image_theme.status_icons[account.status])
                self.setTabIcon(index, icon)
                self.setTabText(index, unicode(account.display_name))

    #[START] -------------------- GUI.BASE.CONVERSATIONMANAGER_OVERRIDE
    def _on_tab_close_request(self, index):
        '''Slot executed when the use clicks the close button in a tab'''
        self.close(self.widget(index))
