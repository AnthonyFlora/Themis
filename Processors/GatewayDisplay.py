from Framework.Themis import EventProcessor
import curses
import time
import signal
import sys
import datetime
import collections


def signal_handler(sig, frame):
    curses.endwin()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


class Display(EventProcessor):
    def __init__(self, event_broker, host):
        EventProcessor.__init__(self, event_broker)
        self.processor = self.processor + '_' + host
        self.host = host
        self.screen = curses.initscr()
        self.setup_curses()
        self.rows, self.cols = self.screen.getmaxyx()
        self.set_event_handler('log', self.on_log_event)
        self.model = collections.defaultdict()

    def refresh(self):
        curses.curs_set(0)
        self.refresh_gateway_status()
        self.refresh_site_survey()
        self.screen.clrtoeol()
        self.screen.refresh()

    def refresh_gateway_status(self):
        table = '%-20s  %-24s  %-16s  %-20s  %-50s'
        title = ('Gateway', 'Address', 'Status', 'Last Update', 'Utilization')
        delim = ('-' * 20, '-' * 24, '-' * 16, '-' * 20, '-' * 50)
        value = ('pi-gate', '00:00:00:00:00:00:00:00', 'ONLINE', '1549165638.000000', '|')
        self.screen.addstr(0, 0, '%-140s' % ('  Gateway Status'), curses.color_pair(2))
        self.screen.addstr(2, 2, table % title, curses.color_pair(1))
        self.screen.addstr(3, 2, table % delim, curses.color_pair(1))
        self.screen.addstr(4, 2, table % value, curses.color_pair(1))
        self.screen.addstr(5, 2, table % value, curses.color_pair(1))
        self.screen.addstr(6, 2, table % value, curses.color_pair(1))
        self.screen.addstr(7, 2, table % value, curses.color_pair(1))

    def refresh_site_survey(self):
        table = '%-20s  %-24s  %-16s  %-16s  %-16s  %-16s  %-16s'
        title = ('ESSID', 'Address', 'Signal(G1)', 'Signal(G2)', 'Signal(G3)', 'Signal(G4)', 'Signal(G5)')
        delim = ('-' * 20, '-' * 24, '-' * 16, '-' * 16, '-' * 16, '-' * 16, '-' * 16)
        value = ('pi-gate', '00:00:00:00:00:00:00:00', '87', '33', '22', '22', '1')
        self.screen.addstr(9, 0, '%-140s' % ('  Site Survey'), curses.color_pair(2))
        self.screen.addstr(11, 2, table % title, curses.color_pair(1))
        self.screen.addstr(12, 2, table % delim, curses.color_pair(1))
        self.screen.addstr(13, 2, table % value, curses.color_pair(1))
        self.screen.addstr(14, 2, table % value, curses.color_pair(1))
        self.screen.addstr(15, 2, table % value, curses.color_pair(1))
        self.screen.addstr(16, 2, table % value, curses.color_pair(1))
        self.screen.addstr(17, 2, table % value, curses.color_pair(1))
        self.screen.addstr(18, 2, table % value, curses.color_pair(1))
        self.screen.addstr(19, 2, table % value, curses.color_pair(1))
        self.screen.addstr(20, 2, table % value, curses.color_pair(1))
        self.screen.addstr(21, 2, table % value, curses.color_pair(1))
        self.screen.addstr(22, 2, table % value, curses.color_pair(1))
        self.screen.addstr(23, 2, table % value, curses.color_pair(1))
        self.screen.addstr(24, 2, table % value, curses.color_pair(1))
        self.screen.addstr(25, 2, table % value, curses.color_pair(1))

    def setup_curses(self):
        curses.noecho()  # no keyboard echo
        curses.cbreak()  # don't wait for newline
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
            curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)
            curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE)

    def on_log_event(self, event):
        processor = event.data['processor']
        log_entry = event.data['entry']
        entry = '%s : %s -> %s' % (datetime.datetime.now(), processor, log_entry)
        self.refresh()

