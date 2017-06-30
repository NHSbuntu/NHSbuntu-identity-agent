import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


"""
Hacky class to produce a PIN dialog window
"""
class PinDialog(Gtk.Window):

    def __init__(self, parent):
        Gtk.Window.__init__(self, title="Enter SmartCard PIN")
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_keep_above(True)
        self.add(box)
        self.set_border_width(10)
        labelbox = Gtk.Box(spacing=10)
        entrybox = Gtk.Box(spacing=5)
        msgbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        buttonbox = Gtk.Box(spacing=5)

        box.pack_start(labelbox, True, True, 10)
        box.pack_start(entrybox, True, True, 0)
        box.pack_start(msgbox, True, True, 20)
        box.pack_start(buttonbox, True, True, 0)

        image = Gtk.Image.new_from_file("nhsbuntu.png")
        labelbox.add(image)

        label = Gtk.Label("Log in with SmartCard")
        label2 = Gtk.Label("Enter your passcode...")
        label3 = Gtk.Label("By entering your passcode you confirm your acceptance")
        label4 = Gtk.Label("of the NHS Care Identity Sevice terms and conditions.")
        self.entry = Gtk.Entry()
        self.entry.set_text("")
        self.entry.set_visibility(False)
        entrybox.add(label2)
        entrybox.add(self.entry)
        msgbox.add(label3)
        msgbox.add(label4)

        self.ok = Gtk.Button("OK")
        buttonbox.add(self.ok)
        buttonbox.set_child_packing(self.ok, False, False, 0, Gtk.PackType.END)
        self.ok.set_property("width-request", 100)

        self.cancel = Gtk.Button("Cancel")
        buttonbox.add(self.cancel)
        buttonbox.set_child_packing(self.cancel, False, False, 0, Gtk.PackType.END)
        self.cancel.set_property("width-request", 100)

        self.show_all()

    def register_ok(self, func):
        self.ok.connect("clicked", func)

    def register_cancel(self, func):
        self.cancel.connect("clicked", func)

"""
Class for Role Selector Dialog
""" 
class RoleSelectDialog(Gtk.Window):
    def __init__(self, parent):
        Gtk.Window.__init__(self, title="Select Your Role")
        self.set_border_width(10)
        self.set_default_size(250,500)

        self.roles = []
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        buttonbox = Gtk.Box(spacing=5)        
 
        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box_outer.pack_start(scrolled, True, True, 0)
        box_outer.pack_start(buttonbox, False, False, 0)
        self.add(box_outer)

        self.listbox = Gtk.ListBox()
        #self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        scrolled.add(self.listbox)
        #self.listbox.connect('row-activated', lambda widget, row: widget.role_id = row.data)

        #box_outer.pack_start(buttonbox, True, True, 0)

        self.ok = Gtk.Button("OK")
        buttonbox.add(self.ok)
        buttonbox.set_child_packing(self.ok, False, False, 0, Gtk.PackType.END)
        self.ok.set_property("width-request", 100)

        self.cancel = Gtk.Button("Cancel")
        buttonbox.add(self.cancel)
        buttonbox.set_child_packing(self.cancel, False, False, 0, Gtk.PackType.END)
        self.cancel.set_property("width-request", 100)

    def register_ok(self, func):
        self.ok.connect("clicked", func)

    def register_cancel(self, func):
        self.cancel.connect("clicked", func)


    def add_roles(self, roles):
        self.roles = roles
        for role in roles:
            self._add_role_to_listbox(role["org_name"] + " : " + 
                                      role["org_code"] + " : " + 
                                      role["name"], role["id"])

    def _add_role_to_listbox(self, role, role_id):
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        label = Gtk.Label(role)
        hbox.pack_start(label, False, False, 0)
        hbox.set_border_width(10)
        row.add(hbox)
        row.data = role_id
        self.listbox.add(row)

"""
Tiny main window - required as hack to allow quitting the IA given we can't use an 
app indicator.

TODO Need to work out how to make it work in gnome shell without this
"""
class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="NHSD Identity Agent")
        self.set_icon_from_file("ia.svg")
        self.set_default_size(250,0)
        self.set_border_width(0)

