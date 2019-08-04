import asyncio
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

loop = asyncio.get_event_loop()

cube = HomeeCube(options.cube, options.username, options.password)

nodes = []

def print_attribute(node, attribute):
    if attribute:
        print("Update attribute %s (type %s): %s " % (attribute.id, attribute.type, attribute.value))

def print_node(node):
    print("New node {}: {}".format(node.id, node.name))
    cube.register(node, print_attribute)

cube.register_all(print_node)

client_task = loop.create_task(cube.run())
try:
    loop.run_forever()

except KeyboardInterrupt:
    client_task.cancel()  # modified line

    pending = asyncio.Task.all_tasks()
    try:
        loop.run_until_complete(asyncio.gather(*pending))
    except asyncio.CancelledError:
        pass

    print('All tasks concluded.')

