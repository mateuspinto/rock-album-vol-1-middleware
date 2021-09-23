import Pyro5.api


@Pyro5.api.expose
class GreetingMaker(object):
    def get_fortune(self, name):
        return "Hello, {0}. Here is your fortune message:\n" \
               "Tomorrow's lucky number is 12345678.".format(name)


daemon = Pyro5.server.Daemon()
ns = Pyro5.api.locate_ns()
uri = daemon.register(GreetingMaker)
ns.register("example.greeting", uri)

print("Ready.")
daemon.requestLoop()
