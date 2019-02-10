import signal
from optparse import OptionParser
from pyhomee import HomeeCube
import logging

parser = OptionParser()
parser.add_option("-c", "--cube", dest="cube",
                  help="hostname of Homee Cube")
parser.add_option("-u", "--username",
                  dest="username",
                  help="Username to connect to Cube")
parser.add_option("-p", "--password",
                  dest="password",
                  help="Password to connect to Cube")

(options, args) = parser.parse_args()
logging.basicConfig(level=logging.DEBUG)
required = "cube username password".split()

for r in required:
    if options.__dict__[r] is None:
        parser.error("parameter %s required"%r)

cube = HomeeCube(options.cube, options.username, options.password)

print("Connected")

def signal_handler(signal, frame):
    cube.stop()


signal.signal(signal.SIGINT, signal_handler)


def print_attribute(attribute):
    print("Update attribute %s (type %s): %s " % (attribute.id, attribute.type, attribute.value))


nodes = cube.get_nodes()
for node in nodes:
    cube.register(node, print_attribute)
