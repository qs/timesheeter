import gtk
import appindicator
import sys
from datetime import datetime, timedelta


STATUS_MESSAGE_LENGTH = 50
MESSAGE_SPLIT_LENGTH = 40
STATUS_UPDATE_FREQUENCY = 60 * 1000  # in milliseconds
MESSAGE_ON_BREAK = 'You are on break'


class TimeSheeter(object):
    def __init__(self):
        self.message = ''
        self.context_status = ''
        self.since = datetime.now()

        self.indicator = appindicator.Indicator("timesheeter-iow",
                                                "application-running",
                                                appindicator.CATEGORY_APPLICATION_STATUS)
        self.indicator.set_status(appindicator.STATUS_ACTIVE)
        self.menu = gtk.Menu()
        self.menu_items = {}
        self.menu_setup()
        self.set_message(MESSAGE_ON_BREAK)

    def menu_setup(self):
        self.update_context_status()
        goto_ticket_item = gtk.MenuItem(self.context_status)
        goto_ticket_item.connect("activate", self.action_goto_ticket)
        settings_item = gtk.MenuItem("Settings")
        settings_item.connect("activate", self.action_settings)
        quit_item = gtk.MenuItem("Quit")
        quit_item.connect("activate", self.action_quit)
        set_ticket_item = gtk.MenuItem("Take a break")
        set_ticket_item.connect("activate", self.action_quit)

        item_list = [
            goto_ticket_item,
            gtk.SeparatorMenuItem(),
            set_ticket_item,
            gtk.SeparatorMenuItem(),
            settings_item,
            quit_item
        ]

        for item in item_list:
            item.show()
            self.menu.append(item)
        self.indicator.set_menu(self.menu)

    def update_context_status(self):
        message = ''
        if self.message:
            line_len = 0
            words = self.message.split(" ")
            for word in words:
                if line_len + len(word) > MESSAGE_SPLIT_LENGTH:
                    message += "\n"
                    line_len = 0
                message += word + " "
                line_len += len(word)
        else:
            message = MESSAGE_ON_BREAK
        delta = datetime.now() - self.since
        delta = '{0}h {1}m'.format(*str(delta).split(':')[:2])
        message += "\n  Since: {0}, {1}".format(self.since.strftime("%H:%M"), delta)
        self.context_status = message

    def set_message(self, message):
        self.message = message
        message = message if len(message) < STATUS_MESSAGE_LENGTH \
            else message[:STATUS_MESSAGE_LENGTH] + ".."
        self.indicator.set_label(message)

    def action_goto_ticket(self, widget):
        pass

    def action_set_task(self, widget):
        self.set_message("#111111: Investigating with something really strange and dangerous.")

    def action_quit(self, widget):
        sys.exit(0)

    def action_settings(self, widget):
        pass

    def run(self):
        gtk.main()

if __name__ == "__main__":
    indicator = TimeSheeter()
    gtk.timeout_add(STATUS_UPDATE_FREQUENCY, indicator.update_context_status)
    indicator.run()