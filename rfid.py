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

    # hexcode
    # 0xFF = connects vid the cardreader
    # 0xCA = the verb for "get data"
    # 0x00 (Parameter) 1 = specify which data to get
    # 0x00 (Parameter) 2 = not really needed fo easier commandos (changeable later)
    # 0x00 (last) = how many letters/numbers we will get back. 00 = send back the whole number.
    get_card_id = [0xFF, 0xCA, 0x00, 0x00, 0x00]

    while True:
        try:
            # connect to the card
            connection = my_reader.createConnection()
            connection.connect()

            # send to card and get answer
            data, sw1, sw2 = connection.transmit(get_card_id)

            # 144 = success
            if sw1 == 144:
                unique_id_number = toHexString(data) # make data readable
                print(f"\n [Discovery Detected!!!] Card id: {unique_id_number}")

                time.sleep(2)
                print("Awaiting next card...")
        
        except Exception:
            # if no card connect then the connection will crasch
            # then we catch the exception here
            time.sleep(0.5)

if __name__ == "__main__": # start read the code here
    start_system()


