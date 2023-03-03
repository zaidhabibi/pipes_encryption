"""
Author: @author Zaid Habibi
Professor: Elmer Salazar
Class: CS 4348 Operating System Concepts
Description:
The Encryption class is used to encrypt and decrypt messages using the Vigenere Cypher. 
The cypher cannot handle non-alphabetical inputs and spaces.

"""
class Encryption:
    def __init__(self):
        self.passkey = ""
        self.keep_looping = True

    def process_command(self, command_line):
        
        command, arg = command_line.strip().split(' ', 1)

        if command == 'PASSKEY':
            self.passkey = arg  
            print('RESULT')

        elif command == 'ENCRYPT':
            if not self.passkey:
                print ('ERROR No passkey set')
            else:
                encrypted = self.encrypt(arg, self.passkey)
                print ('RESULT {}'.format(encrypted))

        elif command == 'DECRYPT':
            if not self.passkey:
                print ('ERROR No passkey set')
            else:
                decrypted = self.decrypt(arg)
                print ('RESULT {}'.format(decrypted))

        elif command == 'QUIT':
            print('RESULT')
            self.keep_looping = False
            

        else:
            print ('ERROR Invalid command: {}'.format(command))


    def encrypt(self, message, key):
       
        # Implement Vigenere cipher encryption algorithm
        if not self.passkey:
            return "ERROR No passkey set"

        while len(key) < len(message):
            key += key
        
        ciphertext = ""

        for  i in range(len(message)):
            m = ord(message[i]) - 65
            k = ord(key[i]) -65
            c = (m + k) % 26
            ciphertext += chr(c + 65)
        
        return ciphertext


    def decrypt(self, message):

        # Split the message into the key and the encrypted text
        parts = message.split(' ', 1)
        if len(parts) != 2:
            return "ERROR Invalid message"
        key = parts[0]
        encrypted_text = parts[1]

        # Implement Vigenere cipher decryption algorithm
        decrypted_text = []
        key_index = 0
        for letter in encrypted_text:
            if letter.isalpha():
                key_letter = key[key_index % len(key)]
                key_value = ord(key_letter.lower()) - 97
                if letter.isupper():
                    decrypted_letter = chr((ord(letter) - key_value - 65) % 26 + 65)
                else:
                    decrypted_letter = chr((ord(letter) - key_value - 97) % 26 + 97)
                key_index += 1
            else:
                decrypted_letter = letter
            decrypted_text.append(decrypted_letter)

        decrypted_text = "".join(decrypted_text)
        return decrypted_text




if __name__ == '__main__':
    enc = Encryption()
    while enc.keep_looping == True:
        try:
            cmd = input().strip()
            enc.process_command(cmd)
        except EOFError:
            break