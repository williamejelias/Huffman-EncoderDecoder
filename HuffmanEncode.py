import collections
from bitarray import bitarray
import pickle
import sys
import time


class NodeTree(object):
    def __init__(self, left_child=None, right_child=None):
        self.left_child = left_child
        self.right_child = right_child

    def children(self):
        return self.left_child, self.right_child


def get_symbol_frequency_map(filename):
    global file_contents
    file_contents = open(filename).read()
    return collections.Counter(list(file_contents)).most_common()


def build_tree(list_of_tuples):
    while len(list_of_tuples) > 1:
        lf, lfw = list_of_tuples.pop()
        slf, slfw = list_of_tuples.pop()
        node = NodeTree(lf, slf)
        new_weight = lfw + slfw
        if len(list_of_tuples) == 0:
            list_of_tuples.insert(0, (node, new_weight))
        else:
            added = False
            for i in range(len(list_of_tuples)):
                if new_weight >= list_of_tuples[i][1]:
                    list_of_tuples.insert(i, (node, new_weight))
                    added = True
                    break
            if added is False:
                list_of_tuples.append((node, new_weight))
    return list_of_tuples


def traverse_get_codewords(node, binstring=""):
    if type(node) is str:
        return {node: binstring}
    (l, r) = node.children()
    codeword_dictionary = dict()
    codeword_dictionary.update(traverse_get_codewords(l, binstring + "0"))
    codeword_dictionary.update(traverse_get_codewords(r, binstring + "1"))
    return codeword_dictionary


def get_bitarray_codewords(dictionary):
    codeword_bitarray_dictionary = {}
    for key, value in dictionary.items():
        codeword = bitarray()
        codeword.extend(value)
        codeword_bitarray_dictionary[key] = codeword
    return codeword_bitarray_dictionary


def encode(text, dictionary):
    output = bitarray()
    output.encode(dictionary, text)
    return output


start = time.time()
infile = sys.argv[1]
filename = infile
try:
    frequencyMap = get_symbol_frequency_map(filename)
    if file_contents == "":
        # file is empty - cannot encode
        print("Selected file is empty and thus cannot be compressed.")
        print("Exiting program")
    else:
        # print("Frequency Map: ", frequencyMap)
        frequencyMapCopy = frequencyMap[:]
        huffmanBitarrayCodes = {}
        if len(frequencyMap) == 1:
            # only one symbol in file
            # make a dictionary with one entry (the symbol) with the value bitarray('0')
            symbol = frequencyMap[0][0]
            value = bitarray('0')
            huffmanBitarrayCodes[symbol] = value
            # print("bitarray codewords: ", huffmanBitarrayCodes)
        else:
            # more than one symbol in file - encode using tree technique
            tree = build_tree(frequencyMap)[0][0]
            huffmanCodes = traverse_get_codewords(tree)
            huffmanBitarrayCodes = get_bitarray_codewords(huffmanCodes)

            # print("huffman codes: ", huffmanCodes)
            # print("bitarray codewords: ", huffmanBitarrayCodes)

            # print(" Char |  Freq  |      Huffman code     ")
            # print("---------------------------------------")
            # for char, frequency in frequencyMapCopy:
            #     print(" %-4r | %6d | %22s" % (char, frequency, huffmanCodes[char]))
            # print()

        output = encode(file_contents, huffmanBitarrayCodes)

        length_of_padded_zeroes = output.fill()
        # print("length_of_padded_zeroes: ", length_of_padded_zeroes)
        # print("output: ", output)

        to_write = [huffmanBitarrayCodes, length_of_padded_zeroes, output]

        newFile = open(('' + filename[:-4] + ".hc"), "wb")
        pickle.dump(to_write, newFile)

        print("Done.")
        print("Number of symbols: ", len(huffmanBitarrayCodes))
        print("Time: ", (time.time() - start))
except FileNotFoundError:
    print("No such file or directory...")
    print("Exiting program.")
