import gtk
import appindicator
import sys
from datetime import datetime, timedelta

STATUS_MESSAGE_LENGTH = 50
MESSAGE_SPLIT_LENGTH = 40
STATUS_UPDATE_FREQUENCY = 60 * 1000  # in milliseconds
MESSAGE_ON_BREAK = 'You are on break'
ON_BREAK = -1


class TimeSheeter(object):
    def __init__(self):
        self.message = ''
        self.context_status = ''
        self.since = None

        self.indicator = appindicator.Indicator("timesheeter-iow",
                                                "application-running",
                                                appindicator.CATEGORY_APPLICATION_STATUS)
        self.indicator.set_status(appindicator.STATUS_ACTIVE)
        self.menu = gtk.Menu()
        self.menu_items = {}

        self.menu_init_setup()
        self.set_activity(ON_BREAK)


    def menu_init_setup(self):
        """
        Initial context menu setup: set menu items.
        """
        self.menu_items['quit'] = gtk.MenuItem("Quit")
        self.menu_items['ticket'] = gtk.MenuItem(self.context_status)
        self.menu_items['settings'] = gtk.MenuItem("Settings")
        self.menu_items['set_ticket'] = gtk.MenuItem("Set new aim")
        self.menu_items['set_break'] = gtk.MenuItem("Take a break")
        for name, item in self.menu_items.iteritems():
            item.connect('activate', getattr(self, 'action_{0}'.format(name)))
        menu_order = [
            self.menu_items['ticket'],
            gtk.SeparatorMenuItem(),
            self.menu_items['set_ticket'],
            self.menu_items['set_break'],
            gtk.SeparatorMenuItem(),
            self.menu_items['settings'],
            self.menu_items['quit']
        ]
        for item in menu_order:
            item.show()
            self.menu.append(item)
        self.indicator.set_menu(self.menu)

    def set_activity(self, ticket_id, message=""):
        """
        Set new activity: update message and context message and since time.
        If provided ticket is ON_BREAK, set on break mode: change menu 'ticket' behavior to
        set new activity.
        If previous activity was ON_BREAK, change menu 'ticket' behavior to 'to to ticket'.
        If previous activity was another ticket, log time spent on that activity.
        :param ticket_id: real ticket id from URL or ON_BREAK
        :type ticket_id: int
        """
        self.since = datetime.now()
        if ticket_id == ON_BREAK:
            self.message = MESSAGE_ON_BREAK
            self.menu_items['set_break'].hide()
        else:
            self.message = message
            self.menu_items['set_break'].show()
        self.update_context_status()

    def update_context_status(self):
        """
        For current message update context menu item
        to split it into multi-line and add since time.
        set self.context_status
        """
        message = ''
        if self.message == MESSAGE_ON_BREAK:
            message = MESSAGE_ON_BREAK
        else:
            line_len = 0
            words = self.message.split(" ")
            for word in words:
                if line_len + len(word) > MESSAGE_SPLIT_LENGTH:
                    message += "\n"
                    line_len = 0
                message += word + " "
                line_len += len(word)
        delta = datetime.now() - self.since
        delta = '{0}h {1}m'.format(*str(delta).split(':')[:2])
        message += "\n  Since: {0}, {1}".format(self.since.strftime("%H:%M"), delta)
        self.context_status = message
        self.menu_items['ticket'].set_label(self.context_status)
        self.set_message(self.message)

    def set_message(self, message):
        self.message = message
        message = message if len(message) < STATUS_MESSAGE_LENGTH \
            else message[:STATUS_MESSAGE_LENGTH] + ".."
        self.indicator.set_label(message)

    def action_quit(self, widget):
        sys.exit(0)

    def action_settings(self, widget):
        """
        Show settings window.
        """
        pass

    def action_ticket(self, widget):
        """
        Open in browser ticket url if it is not ON_BREAK.
        """
        pass

    def action_set_ticket(self, widget):
        """
        Show window for setting ticket URL and aim message
        """
        message = "#111111 Investigating with something strange and dungerous"
        ticket_id = 111111
        self.set_activity(ticket_id, message)

    def action_set_break(self, widget):
        """
        Set break
        """
        self.set_activity(ON_BREAK)

    def run(self):
        gtk.main()


if __name__ == "__main__":
    indicator = TimeSheeter()
    gtk.timeout_add(STATUS_UPDATE_FREQUENCY, indicator.update_context_status)
    indicator.run()