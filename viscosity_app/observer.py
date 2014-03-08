import logging
import types


logger = logging.getLogger(__name__)


class Subject(object):
    """
    Subject -> dispatches messages to interested callables
    """
    def __init__(self):
        self._observers = {}

    def registerObserver(self, observer, events=None):
        """
        register a listener function

        Parameters
        -----------
        observer : external listener function
        events  : tuple or list of relevant events (default=None)
        """
        if events is not None and type(events) not in (types.TupleType,
                                                       types.ListType):
            events = (events,)

        self._observers[observer] = events

    def notifyObservers(self, event=None, msg=None):
        """notify observers """
        for observer, events in list(self._observers.items()):
            if events is None or event is None or event in events:
                try:
                    observer(self, event, msg)
                except (Exception,) as e:  # pylint: disable=W0703
                    #self.unregisterObserver(observer)
                    errmsg = "Exception in message dispatch: Handler '{0}' "
                    "for event '{1}'  ".format(
                                                observer.__class__.__name__,
                                                event)
                    logging.error(errmsg, exc_info=e)

    def unregisterObserver(self, observer):
        """ unregister observer function """
        del self._observers[observer]


class ExampleObserver(object):
    def __init__(self, name=None):
        self.name = name

    def notify(self, sender, event, msg=None):
        logging.warn("[%s] got event %s with message '%s'",
                     self.name,
                     event,
                     msg)


if __name__ == "__main__":
    print('demonstrating event system')

    alice = Subject()
    bob = ExampleObserver('bob')
    charlie = ExampleObserver('charlie')
    dave = ExampleObserver('dave')

    # add subscribers to messages from alice
    alice.registerObserver(bob.notify, events='event1')  # listen to 'event1'
    alice.registerObserver(charlie.notify, events='event2')  # listen to 'event2'
    alice.registerObserver(dave.notify)  # listen to all events

    # dispatch some events
    alice.notifyObservers(event='event1')
    alice.notifyObservers(event='event2', msg=[1, 2, 3])
    alice.notifyObservers(msg='attention to all')

    print 'Done.'
