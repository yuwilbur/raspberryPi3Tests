class Event(object):
    def __init__(self, event_type, data=None):
        self._type = event_type
        self._data = data

    def type(self):
        return self._type

    def data(self):
        return self._data

class EventDispatcher(object):
    def __init__(self):
        self._events = dict()

    def __del__(self):
        self._events = None

    def has_listener(self, event_type, listener):
        if event_type in self._events.keys():
            return listener in self._events[event_type]
        else:
            return False

    def add_event_listener(self, event_type, listener):
        if not self.has_listener(event_type, listener):
            if not event_type in self._events.keys():
                self._events[event_type] = []
            self._events[event_type].append(listener)

    def remove_event_listener(self, event_type, listener):
        if self.has_listener(event_type, listener):
            self._events[event_type].remove(listener)
            if len(self._events[event_type]) == 0:
                del self._events[event_type]

    def dispatch_event(self, event):
        if event.type() in self._events.keys():
            for listener in self._events[event.type()]:
                listener(event)

class MyEvent(Event):
    ASK = 'askMyEvent'
    RESPOND = 'respondMyEvent'

class WhoAsk(object):
    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.event_dispatcher.add_event_listener(MyEvent.RESPOND, self.on_answer_event)

    def ask(self):
        print ">>> I'm instance {0}. Who are listening to me ?".format(self)
        self.event_dispatcher.dispatch_event(Event(MyEvent.ASK, self))

    def on_answer_event(self, event):
        print "<<< Thank you instance {0}.".format(event.data())

class WhoRespond(object):
    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.event_dispatcher.add_event_listener(MyEvent.ASK, self.on_ask_event)

    def on_ask_event(self, event):
        self.event_dispatcher.dispatch_event(Event(MyEvent.RESPOND, self))


dispatcher = EventDispatcher()
who_ask = WhoAsk(dispatcher)
who_respond1 = WhoRespond(dispatcher)
who_respond2 = WhoRespond(dispatcher)
who_ask.ask()
