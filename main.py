class transistor:
    def __init__(self, _signal=False):
        self.state = _signal

    def send_signal(self, _signal):
        self.state = bool(_signal)

    def get_state(self):
        return self.state


class not_gate:
    def __init__(self, _signal=False):
        self.state = not _signal

    def send_signal(self, _signal):
        self.state = not _signal

    def get_state(self):
        return self.state


class and_gate:

    def __init__(self, _signal1=False, _signal2=False):
        self.t1 = transistor(_signal1)
        self.t2 = transistor(_signal2)
        self.state = True if self.t1.get_state() and self.t2.get_state() else False

    def send_signal(self, _signal1, _signal2):
        self.t1.send_signal(_signal1)
        self.t2.send_signal(_signal2)
        self.state = True if self.t1.get_state() and self.t2.get_state() else False

    def get_state(self):
        return self.state


class or_gate:

    def __init__(self, _signal1=False, _signal2=False):
        self.t1 = transistor(_signal1)
        self.t2 = transistor(_signal2)
        self.state = True if self.t1.get_state() or self.t2.get_state() else False

    def send_signal(self, _signal1, _signal2):
        self.t1.send_signal(_signal1)
        self.t2.send_signal(_signal2)
        self.state = True if self.t1.get_state() or self.t2.get_state() else False

    def get_state(self):
        return self.state


class xor_gate:

    def __init__(self, _signal1=False, _signal2=False):
        self.t1 = transistor(_signal1)
        self.t2 = transistor(_signal2)
        if self.t1.get_state() and self.t2.get_state():
            self.state = False
        elif self.t1.get_state() or self.t2.get_state():
            self.state = True
        else:
            self.state = False

    def send_signal(self, _signal1, _signal2):
        self.t1.send_signal(_signal1)
        self.t2.send_signal(_signal2)
        if self.t1.get_state() and self.t2.get_state():
            self.state = False
        elif self.t1.get_state() or self.t2.get_state():
            self.state = True
        else:
            self.state = False

    def get_state(self):
        return self.state


if __name__ == '__main__':

    xorGate1 = xor_gate()

    print(xorGate1.get_state())

    xorGate1.send_signal(1, 0)

    print(xorGate1.get_state())

    xorGate1.send_signal(1, 1)

    print(xorGate1.get_state())

    xorGate1.send_signal(0, 1)

    print(xorGate1.get_state())

    xorGate1.send_signal(0, 0)

    print(xorGate1.get_state())
