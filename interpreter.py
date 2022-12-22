class InterpreterException(Exception):
  ...


COMMANDS = ['MoO', 'MOo', 'moO', 'mOo', 'moo',
            'MOO', 'OOM', 'oom', 'mOO', 'Moo', 'OOO']


class Memory:
  def __init__(self, size) -> None:
    self._size = size
    self._memory = [0 for _ in range(0, size)]
    self._memory_pointer = 0

  def forward(self):
    if self._memory_pointer == self._size:
      self._memory_pointer = 0
    else:
      self._memory_pointer += 1

  def backward(self):
    if self._memory_pointer == 0:
      self._memory_pointer = self._size
    else:
      self._memory_pointer -= 1

  def set(self, value):
    self._memory[self._memory_pointer] = value

  def get(self):
    return self._memory[self._memory_pointer]


class Interpreter:
  def __init__(self) -> None:
    self._memory = Memory(100)
    self._commands = []
    self._command_pointer = 0
    self._cycles = []

  def eval(self, text):
    self._commands = text.split()
    self._cycles = self.find_cycles(self._commands)

    while self._command_pointer < len(self._commands):
      self.exec_command(self._commands[self._command_pointer])
      self._command_pointer += 1

  def find_cycles(self, commands: list):
    commands = commands.copy()
    cycles = []

    while 'MOO' in commands and 'moo' in commands:
      command_pointer = 0
      cycle_start = 0

      while True:
        match commands[command_pointer]:
          case 'MOO':
            cycle_start = command_pointer
          case 'moo':
            cycles.append(cycle_start)
            cycles.append(command_pointer)

            commands[cycle_start] = commands[command_pointer] = None

            break

        command_pointer += 1

    if 'moo' in commands:
      raise InterpreterException(
          f"Unexpected moo at index {commands.index('moo')}")

    if 'MOO' in commands:
      raise InterpreterException(
          f"Unexpected MOO at index {commands.index('MOO')}")

    return cycles

  def exec_command(self, command):
    match command:
      case 'MoO':
        self._memory.set(self._memory.get() + 1)

      case 'MOo':
        self._memory.set(self._memory.get() - 1)

      case 'moO':
        self._memory.forward()

      case 'mOo':
        self._memory.backward()

      case 'moo':
        pos = self._cycles.index(self._command_pointer) - 1
        self._command_pointer = self._cycles[pos] - 1

      case 'MOO':
        if self._memory.get() == 0:
          pos = self._cycles.index(self._command_pointer) + 1
          self._command_pointer = self._cycles[pos]

      case 'OOM':
        print(self._memory.get(), end='')

      case 'oom':
        self._memory.set(int(input()))

      case 'mOO':
        command_index = self._memory.get()

        if command_index < len(COMMANDS):
          raise InterpreterException(
              f"No such command index -> {command_index}")

        if command_index == 8:
          raise InterpreterException(
              f"You can't execute mOO command by itself")

        self.eval(COMMANDS[command_index])

      case 'Moo':
        if (self._memory.get() == 0):
          self._memory.set(input(int))
        else:
          print(chr(self._memory.get()), end='')

      case 'OOO':
        self._memory.set(0)

      case _:
        raise InterpreterException(f"No such command -> {command}")
