from smartcard.System import readers
from smartcard.Exceptions import NoCardException
import time
from smartcard.util import toHexString

def explore_card():
    found_reader = readers()
    if not found_reader:
        print("Did not find reader.")
        return
    
    reader = found_reader[0]
    print(f" Connected to {reader}")
    print("\nShow card to try unlock sektor 1 (block 4)...")

    # APDU 1: Ladda in vår "Master Key" (Standardnyckeln) i läsarens minne
    # 0xFF, 0x82 = Kommandot för att ladda en nyckel
    # 0x00, 0x00 = Spara nyckeln på minnesplats 0 i läsaren
    # 0x06 = Nyckelns längd är 6 bytes
    # De sista 6 är själva nyckeln (FF FF FF FF FF FF)
    load_key_cmd = [0xFF, 0x82, 0x00, 0x00, 0x06, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

    # APDU 2: Försök logga in på blocket
    # 0xFF, 0x86 = Kommandot för att autentisera
    # 0x04 = Vilket block vi vill låsa upp (Block 4 är början på Sektor 1)
    # 0x60 = Vi vill logga in med "Nyckel A" (Standard för att läsa data)
    # 0x00 = Hämta nyckeln från minnesplats 0 i läsaren
    auth_cmd = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, 0x04, 0x60, 0x00]

    while True:
        try:
            connection = reader.createConnection()
            connection.connect()

            # send key to reader
            data, status_word_1, status_word_2 = connection.transmit(load_key_cmd)

            # 144 = success is decimal for 0x90
            if status_word_1 == 144:
                print("\n[+] Standardkey loaded in reader.")
            else:
                print("\n[-] Reader refused to take the key.")

            # try to unlock block 4
            data, status_word_1, status_word_2 = connection.transmit(auth_cmd)

            if status_word_1 == 144:
                print("[!] SUCCESS! Sektor 1 unlocked. We got access to memory.")
                #HÄR LÄGGER VI TILL KODEN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            else:
                # Om kortet har bytt nyckel från standard får vi ett fel (t.ex. 99)
                print(f"[-] Rejected. Card is using another key. (Errorcode: {status_word_1})")

            time.sleep(3)
            print("\nwaiting for next card...")

            connection.disconnect()
    
        except NoCardException: # check if card is on reader
            time.sleep(0.5)
        except Exception as e:
            print(f"An error occured: {e}")
            time.sleep(1)

if __name__ == "__main__":
    explore_card()