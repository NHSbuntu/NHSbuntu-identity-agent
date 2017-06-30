#!/usr/bin/python3
# Hacked together Python 3 GTK+ based IA.
#
# Ramen Sen (ramen.sen@nhs.net)

import os
import threading
import time
import httplib2
import signal
import sys
from urllib.parse import quote

from authenticator import authenticator
from nhsdiaui import PinDialog, MainWindow, RoleSelectDialog
from scard import SmartCardReader

# Windowing stuff
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
require_version('Notify', '0.7')
from gi.repository import Notify as notify

# Not using the app indicator stuff as it doesn't work on Gnome Shell
# Much nicer in Unity though - sigh
#require_version('AppIndicator3', '0.1')
#from gi.repository import AppIndicator3 as appindicator

class IdentityAgentApplication(object):
    APPINDICATOR_ID = 'nhsd-ia'

    def __init__(self):
        self.mainWindow = MainWindow()
        self.mainWindow.connect("delete-event", self.quit)
        self.reader = SmartCardReader()
        self.mainWindow.show_all()
        self.init_security_listener()
        notify.init(self.APPINDICATOR_ID)
        self.poll = True
        self.dialog = PinDialog(self.mainWindow)
        self.dialog.hide()
        self.dialog.register_ok(self.handle_ok)
        self.dialog.register_cancel(self.handle_cancel)
        time.sleep(2) # wait in case card is already inserted
        self.start_card_listener()
        self.auth = authenticator()

    def start_card_listener(self):
        tmp = threading.Thread(target=self.card_events, args=(id,))
        tmp.start()

    def card_events(self, threadname):
        card = False
        while(True):
            check = self.reader.is_card_inserted(timeout=1)
            if check != card:
                card = check
                if check:
                    self.handle_card_insertion()
                else:
                    self.handle_card_removal()
            if not self.poll:
                break

    def handle_card_insertion(self):
        self.dialog.show()

    def handle_card_removal(self):
        notify.Notification.new("Card removed!", None, None).show()
        self.set_security_listener_token("")
        self.dialog.hide()

    def handle_cancel(self, val):
        self.dialog.entry.set_text("")
        self.dialog.hide()

    def handle_ok(self, val):
        self.dialog.hide()
        pin = self.dialog.entry.get_text()
        self.dialog.entry.set_text("")
        try:
            self.response=self.auth.authenticate(pin)
            notify.Notification.new("Authentication successful.", None, None).show()
            self.set_security_listener_token(self.response["sso_ticket"])
        except IndexError:
            notify.Notification.new("Sorry, authentication failed. Remove card and try again.", None, None).show()
            return
        # TODO Now show role selection box
        # put selected role_id into self.roledialog.role_id
        self.roledialog = RoleSelectDialog(self.mainWindow)
        self.roledialog.add_roles(self.response["roles"])
        self.roledialog.show_all()
        self.roledialog.register_ok(self.handle_role_select_ok)
        self.roledialog.register_cancel(self.handle_role_select_cancel)
        self.roledialog.show()

    def handle_role_select_cancel(self, val):
        self.set_security_listener_token("")
        self.roledialog.destroy()
    
    def handle_role_select_ok(self, val):
        role_id = self.roledialog.listbox.get_selected_row().data
        self.auth.role_select(self.response, role_id)
        self.roledialog.destroy()


    def set_security_listener_token(self, token, do_notify=True):
        h = httplib2.Http(ca_certs='ca.crt')
        token = quote(token)
        try:
            (resp, content) = h.request("https://msg.int.spine2.ncrs.nhs.uk:20006/set_ticket/" + token, "PUT",
                                headers={'referer': 'https://ia.spine2.ncrs.nhs.uk'})
        except ConnectionRefusedError:
            if do_notify:
                notify.Notification.new("IA ticket server not running.", None, None).show()
            

    def init_security_listener(self):
        pass


    def quit(self, source, val):
        self.poll = False
        notify.uninit()
        gtk.main_quit()
        self.set_security_listener_token("", do_notify=False)


if __name__ == "__main__":

    # Handle clean exit even if Ctrl-C has been pressed
    def signal_handler(signal, frame):
        IA.quit(None, None)
    signal.signal(signal.SIGINT, signal_handler)

    IA = IdentityAgentApplication()
    gtk.main()



