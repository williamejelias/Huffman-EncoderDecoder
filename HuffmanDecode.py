import pickle
import sys
import time

start = time.time()
infile = sys.argv[1]
filename = infile
try:
    # read the file as bytes and unpickle
    file = open(filename, "rb")
    list_dictionary_message = pickle.load(file)

    # extract dictionary
    huffmanCodes = list_dictionary_message[0]

    # extract the number of padded zeroes
    lengthPaddedZeroes = list_dictionary_message[1]

    # extract the encoded bitarray
    bitarray = list_dictionary_message[2]

    # remove the padded zeroes from the encoded bitarray
    for i in range(lengthPaddedZeroes):
        bitarray.pop()

    # decode the bitarray into a list of characters
    dec = bitarray.decode(huffmanCodes)

    # join the characters into one string to complete the decoding
    decoded_message = ''.join(dec)
    # print("Decoded Message by decode method: ", decoded_message)

    # write the decoded message to a new text file
    newFilename = '' + filename[:-3] + '.txt'
    newFile = open(newFilename, "w")
    newFile.write(decoded_message)

    # close the newly created file
    newFile.close()
    print("Number of symbols: ", len(huffmanCodes))
    print("Time: ", (time.time() - start))

except FileNotFoundError:
    print("No such file or directory...")
    print("Exiting program.")
except pickle.UnpicklingError:
    print("Error decompressing - file is likely corrupted or not in the correct format.")
    print("Exiting program.")
