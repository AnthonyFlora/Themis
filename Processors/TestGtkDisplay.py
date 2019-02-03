from Framework.Themis import EventProcessor
import gtk
import datetime
import gobject


actresses = [ \
    ('rachel weiss', 'london', '1971'), \
    ('scarlett johansson', 'new york', '1984' )]


class Display(EventProcessor):
    def __init__(self, event_broker, host):
        EventProcessor.__init__(self, event_broker)
        self.processor = self.processor + '_' + host
        self.host = host
        self.setupWindow()
        self.set_event_handler('log', self.on_log_event)

    def on_log_event(self, event):
        processor = event.data['processor']
        log_entry = event.data['entry']
        entry = '%s : %s -> %s' % (datetime.datetime.now(), processor, log_entry)
        #gobject.idle_add(self.label.set_label, entry)

    def setupWindow(self):
        self.window = gtk.Window()
        self.window.set_title('Display')
        self.window.set_size_request(350, 250)
        self.window.connect('destroy', gtk.main_quit)

        vbox = gtk.VBox(False, 8)
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(sw, True, True, 0)

        store = self.create_model()
        treeView = gtk.TreeView(store)
        treeView.connect('row-activated', self.on_activated)
        treeView.set_rules_hint(True)
        sw.add(treeView)

        self.create_columns(treeView)
        self.window.statusbar = gtk.Statusbar()
        vbox.pack_start(self.window.statusbar, False, False, 0)
        self.window.add(vbox)
        self.window.show_all()

    def create_model(self):
        store = gtk.ListStore(str, str, str)

        for act in actresses:
            store.append([act[0], act[1], act[2]])

        return store

    def create_columns(self, treeView):
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Name", rendererText, text=0)
        column.set_sort_column_id(0)
        treeView.append_column(column)

        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Place", rendererText, text=1)
        column.set_sort_column_id(1)
        treeView.append_column(column)

        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Year", rendererText, text=2)
        column.set_sort_column_id(2)
        treeView.append_column(column)

    def on_activated(self, widget, row, col):
        model = widget.get_model()
        text = model[row][0] + ", " + model[row][1] + ", " + model[row][2]
        self.window.statusbar.push(0, text)
