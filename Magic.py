from smartcard.System import readers
from smartcard.util import toHexString

def test_magic_card():
    found_reader = readers()
    if not found_reader:
        print("Found no readers")
        return
    
    my_reader = found_reader[0]
    print(f"System is ready, connected to: {my_reader}")
    print("\nPut on ur card u wanna override")
    print("\nWaiting for card...(press ctrl + c to shutdown)")

    input("Press enter when card is on reader")

    try:
        connection = my_reader.createConnection()
        connection.connect()

        # Load standard key
        # 0x = this will be hexadecimal
        # 0xFF = connects vid the cardreader
        # 0x82 = (verv) load a key in ur memory
        # 0x00 = what kind of key?
        # 0x00 = what memory place? (first one)
        # 0x06 = how long is key?
        # 0xFF = the actuall key (used by 9 out of 10 cards)
        load_key = [0xFF, 0x82, 0x00, 0x00, 0x06, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        data, status_word_1, status_word_2 = connection.transmit(load_key)

        if status_word_1 != 144:
            print("Could not load key from the reader")
            return
        
        # Autenthicate against block 0 where key hides
        # 0xFF = get readers atention
        # 0x86 = log in/ authenticate
        # 0x00, 0x00 = ordinary fill in, just in case
        # 0x05 = the following instruction is 5 letters long
        # 0x01 = number of version
        # 0x60 = keytype to log on
        # 0x00 = get key from number 0 where we put it last
        auth_block_0 = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, 0x00, 0x60, 0x00]
        data, status_word_1, status_word_2 = connection.transmit(auth_block_0)
        if status_word_1 != 144:
            print("\n[RESULT]: LOCKED Card refused to unlock Block 0.")
            return
        
        # 3. Try writing to Block 0 (we try to write ID: 01 02 03 04)
        # Last 16 bytes are the new number + security codes (BCC)
        # 0x01, 0x02, 0x03, 0x04 = this is our new number
        # 0x04 = BCC (block check character) check if id-number is not damaged
        # 0x08, 0x04, 0x00 = tells reader what kind of card it is
        # rest is fill in
        new_block_0 = [
            0xFF, 0xD6, 0x00, 0x00, 0x10,  
            0x01, 0x02, 0x03, 0x04,        
            0x04,                          
            0x08, 0x04, 0x00,              
            0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08 
        ]

        print("Authentication succeded! Trying to write the new id to the card...")
        data, status_word_1, status_word_2 = connection.transmit(new_block_0)

        if status_word_1 == 144:
            print("\n[RESULTS]: SUCCESS! U have cloned the card! ID is changed .")
        else:
            print(f"\n[RESULTS]: Could not override card but could log in.")
            print("Its a locked card.")

        connection.disconnect()
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_magic_card()
