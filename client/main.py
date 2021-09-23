import Pyro5.api

name = input("What is your name? ").strip()

greeting_maker = Pyro5.api.Proxy("PYRONAME:example.greeting")
print(greeting_maker.get_fortune(name))
