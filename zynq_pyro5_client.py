import Pyro5.core, Pyro5.client
#import serpent
#import numpy as np
#import matplotlib.pyplot as plt

ns_ip = '192.168.0.2'
ns_port = 4567
ns=Pyro5.core.locate_ns(host=ns_ip,port=ns_port,broadcast=False)
uri=ns.lookup('overlay')
overlay=Pyro5.client.Proxy(uri)

def init_rf_clks(overlay):
    overlay.run('init_rf_clks()')

def get_num_rx_channels(overlay):
    return overlay.len('radio.receiver.channel')

def get_num_tx_channels(overlay):
    return overlay.len('radio.transmitter.channel')

# add your functions here

# load overlay
overlay.load('base.bit')
# initialize clocks
init_rf_clks(overlay)
# example request, get number of rx and tx channels
num_rx_channels = get_num_rx_channels(overlay)
num_tx_channels = get_num_tx_channels(overlay)


