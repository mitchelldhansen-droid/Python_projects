class Signal:
    def __init__(self):
        self._listeners = []

    def connect(self, func):
        self._listeners.append(func)

    def disconnect(self, func):
        if func in self._listeners:
            self._listeners.remove(func)

    def emit(self, *args):
        for func in self._listeners:
            func(*args)
