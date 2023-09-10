print('RFSoC4x2 Server starting up...')
from pynq.overlays.base import BaseOverlay
import Pyro5.server, Pyro5.core, Pyro5.api
import signal, sys
# run server and pyro5 name server on zynq PS device
daemon_ip = '192.168.0.2'
ns_ip = '192.168.0.2'
ns_port = 4567

def signal_handler(signal, frame):
        sys.exit(0)

@Pyro5.api.expose
class OverlayWrapper(object):
    def __init__(self, overlay):
        self.overlay = overlay

    def load(self, string):
        print('Loading overlay: '+string+'...')
        self.overlay = BaseOverlay(string)
        print('Overlay loading complete')

    def run(self, string):
        exec('self.overlay.' + string)

    def write(self, string, val):
        exec('self.overlay.' + string + '=' + str(val))

    def read(self, string):
        return eval('self.overlay.' + string)
    
    def len(self, string):
        return eval('len(self.overlay.' + string +')')

print('Loading overlay: base.bit...')
overlay_wrapped = OverlayWrapper(BaseOverlay("base.bit"))
print('Overlay loading complete')

with Pyro5.server.Daemon(host=daemon_ip) as daemon:
    uri=daemon.register(overlay_wrapped)
    with Pyro5.core.locate_ns(host=ns_ip,port=ns_port) as ns:
        ns.register('overlay',uri)
    print('RFSoC4x2 Pyro 5 Server Running')
    signal.signal(signal.SIGINT,signal_handler)
    daemon.requestLoop()