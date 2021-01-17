class transistor:
    def __init__(self, _signal=False):
        self.state = bool(_signal)

    def send_signal(self, _signal):
        self.state = bool(_signal)
        return self.state

    def get_state(self):
        return self.state


class not_gate:
    def __init__(self, _signal=False):
        self.state = not bool(_signal)

    def send_signal(self, _signal):
        self.state = not bool(_signal)
        return self.state

    def get_state(self):
        return self.state


class and_gate:

    def __init__(self, _signal1=False, _signal2=False):
        self.t1 = transistor(_signal1)
        self.t2 = transistor(_signal2)
        self.state = True if self.t1.get_state() and self.t2.get_state() else False

    def send_signal(self, _signal1, _signal2):
        self.state = True if self.t1.send_signal(_signal1) and self.t2.send_signal(_signal2) else False
        return self.state

    def get_state(self):
        return self.state


class or_gate:

    def __init__(self, _signal1=False, _signal2=False):
        self.t1 = transistor(_signal1)
        self.t2 = transistor(_signal2)
        self.state = True if self.t1.get_state() or self.t2.get_state() else False

    def send_signal(self, _signal1, _signal2):
        self.state = True if self.t1.send_signal(_signal1) or self.t2.send_signal(_signal2) else False
        return self.state

    def get_state(self):
        return self.state


class xor_gate:

    def __init__(self, _signal1=False, _signal2=False):
        self.a1 = and_gate(_signal1, _signal2)
        self.o1 = or_gate(_signal1, _signal2)
        self.n1 = not_gate(self.a1.get_state())
        self.a2 = and_gate(self.n1.get_state(), self.o1.get_state())
        self.state = self.a2.get_state()

    def send_signal(self, _signal1, _signal2):
        self.state = self.a2.send_signal(self.n1.send_signal(self.a1.send_signal(_signal1, _signal2)), self.o1.send_signal(_signal1, _signal2))
        return self.state

    def get_state(self):
        return self.state


class half_adder:

    def __init__(self, _signal1=False, _signal2=False):
        self.x1 = xor_gate(_signal1, _signal2)
        self.a1 = and_gate(_signal1, _signal2)
        self.sum, self.carry = [int(self.x1.get_state()), int(self.a1.get_state())]

    def send_signal(self, _signal1=False, _signal2=False):
        self.sum, self.carry = [int(self.x1.send_signal(_signal1, _signal2)), int(self.a1.send_signal(_signal1, _signal2))]
        return [self.sum, self.carry]

    def get_state(self):
        return [self.sum, self.carry]

    def get_sum(self):
        return self.sum

    def get_carry(self):
        return self.carry

class full_adder:

    def __init__(self, _signal1 = 0, _signal2 = 0, _signal3 = 0):
        self.ha1 = half_adder(_signal1, _signal2)
        self.ha2 = half_adder(self.ha1.get_sum(), _signal3)
        self.o1 = or_gate(self.ha1.get_carry(), self.ha2.get_carry())
        self.sum, self.carry = [int(self.ha2.get_sum()), int(self.o1.get_state())]

    def send_signal(self, _signal1, _signal2, _signal3):
        self.ha1.send_signal(_signal1, _signal2)
        self.ha2.send_signal(self.ha1.get_sum(), _signal3)
        self.o1.send_signal(self.ha1.get_carry(), self.ha2.get_carry())
        self.sum, self.carry = [int(self.ha2.get_sum()), int(self.o1.get_state())]
        return [self.sum, self.carry]

    def get_state(self):
        return [self.sum, self.carry]

    def get_sum(self):
        return self.sum

    def get_carry(self):
        return self.carry

class RipCarryAdder_8:
    def __init__(self, _byte1 = [0,0,0,0,0,0,0,0], _byte2 = [0,0,0,0,0,0,0,0]):
        self.carry_flag = False
        if len(_byte1) == 8 and len(_byte2) == 8:
            self.ha1 = half_adder(int(_byte1[7]), int(_byte2[7]))
            self.fa1 = full_adder(self.ha1.get_carry(), int(_byte1[6]), int(_byte2[6]))
            self.fa2 = full_adder(self.fa1.get_carry(), int(_byte1[5]), int(_byte2[5]))
            self.fa3 = full_adder(self.fa2.get_carry(), int(_byte1[4]), int(_byte2[4]))
            self.fa4 = full_adder(self.fa3.get_carry(), int(_byte1[3]), int(_byte2[3]))
            self.fa5 = full_adder(self.fa4.get_carry(), int(_byte1[2]), int(_byte2[2]))
            self.fa6 = full_adder(self.fa5.get_carry(), int(_byte1[1]), int(_byte2[1]))
            self.fa7 = full_adder(self.fa6.get_carry(), int(_byte1[0]), int(_byte2[0]))
            self.output = [self.fa7.get_sum(), self.fa6.get_sum(), self.fa5.get_sum(), self.fa4.get_sum(), self.fa3.get_sum(), self.fa2.get_sum(), self.fa1.get_sum(), self.ha1.get_sum()]
            self.carry_flag = self.fa7.get_carry()
            if self.carry_flag:
                print("Overflow Warning!")
        else:
            print("Error: arguments must consist of eight binary bits each!")

    def add_bytes(self, _byte1, _byte2):
        if len(_byte1) == 8 and len(_byte2) == 8:
            self.ha1.send_signal(int(_byte1[7]), int(_byte2[7]))
            self.fa1.send_signal(self.ha1.get_carry(), int(_byte1[6]), int(_byte2[6]))
            self.fa2.send_signal(self.fa1.get_carry(), int(_byte1[5]), int(_byte2[5]))
            self.fa3.send_signal(self.fa2.get_carry(), int(_byte1[4]), int(_byte2[4]))
            self.fa4.send_signal(self.fa3.get_carry(), int(_byte1[3]), int(_byte2[3]))
            self.fa5.send_signal(self.fa4.get_carry(), int(_byte1[2]), int(_byte2[2]))
            self.fa6.send_signal(self.fa5.get_carry(), int(_byte1[1]), int(_byte2[1]))
            self.fa7.send_signal(self.fa6.get_carry(), int(_byte1[0]), int(_byte2[0]))
            self.output = [self.fa7.get_sum(), self.fa6.get_sum(), self.fa5.get_sum(), self.fa4.get_sum(), self.fa3.get_sum(), self.fa2.get_sum(), self.fa1.get_sum(), self.ha1.get_sum()]
            self.carry_flag = self.fa7.get_carry()
            if self.carry_flag:
                print("Overflow Warning!")
            return self.output
        else:
            print("Error: arguments must consist of eight binary bits each!")
    
    def get_state(self):
        return [self.output, self.carry_flag]

    def get_byte(self):
        return self.output

    def get_carry(self):
        return self.carry_flag

def byte_to_num_8(_byte):
    total = 0
    if len(_byte) == 8:
        for i in range(len(_byte)):
            if 0 <= int(_byte[i]) < 2:
                total += int(_byte[i])*(2**(7-i))
            else:
                print("Error: argument must be a 0 or a 1!")
        return total
    else:
        print("Error: argument must consist of eight binary bits!")


if __name__ == '__main__':

#Transistor test
    # print("transistor test:")
    # transistor1 = transistor()
    # print(f"default transistor = {transistor1.get_state()}")
    # print(f"updating transistor with signal [1]: {transistor1.send_signal(1)}")
    # print("")

#Not_gate test
    # print("not_gate test:")
    # notGate1 = not_gate()
    # print(f"default not_gate state = {notGate1.get_state()}")
    # print(f"updating not_gate with signal [1]: {notGate1.send_signal(1)}")
    # print("")

#and_gate test
    # print("and_gate test:")
    # andGate1 = and_gate()
    # print(f"default and_gate state = {andGate1.get_state()}")
    # print(f"updating and_gate with signal (1,1): {andGate1.send_signal(1,1)}")
    # print(f"updating and_gate with signal (0,1): {andGate1.send_signal(0,1)}")
    # print(f"updating and_gate with signal (1,0): {andGate1.send_signal(1,0)}")
    # print(f"updating and_gate with signal (0,0): {andGate1.send_signal(0,0)}")
    # print("")

#or_gate test
    # print("or_gate test:")
    # orGate1 = or_gate()
    # print(f"default or_gate state = {orGate1.get_state()}")
    # print(f"updating or_gate with signal (1,1): {orGate1.send_signal(1,1)}")
    # print(f"updating or_gate with signal (0,1): {orGate1.send_signal(0,1)}")
    # print(f"updating or_gate with signal (1,0): {orGate1.send_signal(1,0)}")
    # print(f"updating or_gate with signal (0,0): {orGate1.send_signal(0,0)}")
    # print("")

#xor_gate test
    # print("xor_gate test:")
    # xorGate1 = xor_gate()
    # print(f"default xor_gate state = {xorGate1.get_state()}")
    # print(f"updating xor_gate with signal (1,1): {xorGate1.send_signal(1,1)}")
    # print(f"updating xor_gate with signal (0,1): {xorGate1.send_signal(0,1)}")
    # print(f"updating xor_gate with signal (1,0): {xorGate1.send_signal(1,0)}")
    # print(f"updating xor_gate with signal (0,0): {xorGate1.send_signal(0,0)}")
    # print("")

#half_adder test
    # print("half_adder test:")
    # ha1 = half_adder()
    # print(f"default half_adder state = {ha1.get_state()}")
    # print(f"updating half_adder with signal (0,0): {ha1.send_signal(0,0)}")
    # print(f"updating half_adder with signal (0,1): {ha1.send_signal(0,1)}")
    # print(f"updating half_adder with signal (1,0): {ha1.send_signal(1,0)}")
    # print(f"updating half_adder with signal (1,1): {ha1.send_signal(1,1)}")
    # print(f"half_adder.sum = {ha1.get_sum()}, half_adder.carry = {ha1.get_carry()}")
    # print("")

#full_adder test
    # print("full_adder test:")
    # fa1 = full_adder()
    # print(f"default full_adder state = {fa1.get_state()}")
    # print(f"updating full_adder with signal (0,0,0): {fa1.send_signal(0,0,0)}")
    # print(f"updating full_adder with signal (0,0,1): {fa1.send_signal(0,0,1)}")
    # print(f"updating full_adder with signal (0,1,0): {fa1.send_signal(0,1,0)}")
    # print(f"updating full_adder with signal (1,0,0): {fa1.send_signal(1,0,0)}")
    # print(f"updating full_adder with signal (0,1,1): {fa1.send_signal(0,1,1)}")
    # print(f"updating full_adder with signal (1,1,0): {fa1.send_signal(1,1,0)}")
    # print(f"updating full_adder with signal (1,1,1): {fa1.send_signal(1,1,1)}")
    # print("")

#RipCarryAdder_8 test
    print("8 bit ripple carry adder test:")
    rca8_1 = RipCarryAdder_8()
    # print(f"default : byte = {rca8_1.get_byte()}, carry flag = {rca8_1.get_carry()}")
    byte1 = "00000001"
    byte2 = "00000110"
    rca8_1.add_bytes(byte1,byte2)
    print(f"adding {byte1} & {byte2} gives:\nbyte = {rca8_1.get_byte()}, carry flag = {rca8_1.get_carry()}")
    num1 = byte_to_num_8(byte1)
    num2 = byte_to_num_8(byte2)
    print(f"{num1} + {num2} = {byte_to_num_8(rca8_1.get_byte())}")
