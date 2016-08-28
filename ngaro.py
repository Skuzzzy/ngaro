
class Ngaro():

    def __init__(self):
        self.data = []
        self.address = []
        self.memory = [0] * 1024
        self.instruction_pointer = 0
        self.op_table = {
                0 : self.nop,
                1 : self.lit,
                2 : self.dup,
                3 : self.drop,
                4 : self.swap,
                5 : self.push,
                6 : self.pop,
                7 : self.loop,
                8 : self.jump,
                9 : self.subroutine_return,
                10 : self.gt_jump,
                11 : self.lt_jump,
                12 : self.ne_jump,
                13 : self.eq_jump,
                14 : self.fetch,
                15 : self.store,
                16 : self.add,
                17 : self.subtract,
                18 : self.multiply,
                19 : self.i_divmod,
                20 : self.i_and,
                21 : self.i_or,
                22 : self.xor,
                23 : self.shl,
                24 : self.shr,
                25 : self.zero_exit,
                26 : self.inc,
                27 : self.dec,
                28 : self.i_in,
                29 : self.out
        }

    def execute(self):
        while(self.instruction_pointer < len(self.memory)):
            self.tick()

    def tick(self):
        self.process_opcode()
        self.instruction_pointer = self.instruction_pointer + 1



    def process_opcode(self):
        func = self.op_table[self.memory[self.instruction_pointer]]
        if func:
            func()
        else:
            self.implicit_call()

    def nop(self):
        pass

    def lit(self):
        self.instruction_pointer += 1
        self.data.append(self.memory[self.instruction_pointer])

    def dup(self):
        self.data.append(self.data[-1])

    def drop(self):
        self.data.pop()

    def swap(self):
        top = self.data.pop()
        below = self.data.pop()
        self.data.extend([top, below])

    def push(self):
        self.address.append(self.data.pop())

    def pop(self):
        self.data.append(self.address.pop())

    def loop(self):
        self.data[-1] = self.data[-1] - 1
        self.instruction_pointer += 1
        if self.data[-1] > 0:
            self.instruction_pointer = self.memory[self.instruction_pointer + 1]
        else:
            self.data.pop()

    def jump(self):
        self.instruction_pointer = self.memory[self.instruction_pointer] - 1

    def subroutine_return(self):
        self.instruction_pointer = self.address.pop()

    def gt_jump(self):
        self.instruction_pointer += 1
        first = self.data.pop()
        second = self.data.pop()
        if first > second:
            # self.instruction_pointer = self.memory[self.instruction_pointer] - 1
            self.jump()
        else:
            pass

    def lt_jump(self):
        self.instruction_pointer += 1
        first = self.data.pop()
        second = self.data.pop()
        if first < second:
            # self.instruction_pointer = self.memory[self.instruction_pointer] - 1
            self.jump()
        else:
            pass

    def ne_jump(self):
        self.instruction_pointer += 1
        first = self.data.pop()
        second = self.data.pop()
        if first != second:
            # self.instruction_pointer = self.memory[self.instruction_pointer] - 1
            self.jump()
        else:
            pass

    def eq_jump(self):
        self.instruction_pointer += 1
        first = self.data.pop()
        second = self.data.pop()
        if first == second:
            # self.instruction_pointer = self.memory[self.instruction_pointer] - 1
            self.jump()
        else:
            pass

    def fetch(self):
        lookup = self.memory[self.data.pop()]
        self.data.append(lookup)

    def store(self):
        top = self.data.pop()
        below = self.data.pop()

        self.memory[top] = below

    def add(self):
        top = self.data.pop()
        below = self.data.pop()
        self.data.append(top + below)

    def subtract(self):
        top = self.data.pop()
        below = self.data.pop()
        self.data.append(top - below)

    def multiply(self):
        top = self.data.pop()
        below = self.data.pop()
        self.data.append(top * below)

    def i_divmod(self):
        divisor = self.data.pop()
        dividend = self.data.pop()
        quotient = dividend // divisor
        remainder = dividend % divisor
        self.data.extend([remainder, quotient])

    def i_and(self):
        top = self.data.pop()
        below = self.data.pop()
        self.data.append(top & below)

    def i_or(self):
        top = self.data.pop()
        below = self.data.pop()
        self.data.append(top | below)

    def xor(self):
        top = self.data.pop()
        below = self.data.pop()
        self.data.append(top ^ below)

    def shl(self):
        shift = self.data.pop()
        item = self.data.pop()
        self.data.append(item << shift)

    def shr(self):
        shift = self.data.pop()
        item = self.data.pop()
        self.data.append(item << shift)

    def zero_exit(self):
        if self.data[-1] == 0:
            self.data.pop()
            self.instruction_pointer = self.address.pop()
        else:
            pass

    def inc(self):
        self.data[-1] = self.data[-1] + 1

    def dec(self):
        self.data[-1] = self.data[-1] - 1

    def i_in(self):
        self.data.pop() # TODO
        self.data.append(int(raw_input()))

    def out(self):
        pass
        # TODO

    def wait(self):
        pass
        # TODO

    def implicit_call(self):
        self.address.append(self.instruction_pointer)
        self.instruction_pointer = opcode - 1
