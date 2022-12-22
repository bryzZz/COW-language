from interpreter import Interpreter

with open('files/hello.cow', 'r') as f:
  text = f.read()

  Interpreter().eval(text)
