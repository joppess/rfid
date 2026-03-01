# just testing
from smartcard.System import readers
from smartcard.util import toHexString
import time

def start_system():
    # kollar om vi hittar inkopplat läsare
    found_reader = readers()
    if not found_reader:
        print("Did not find a reader")
        return
    
    my_reader = found_reader[0]
    print(f"System is ready, connected to: {my_reader}")
    print("/nWaiting for card...(press ctrl + c to shutdown)")