# Introduction

In computer science and information theory, a Huffman code is a particular type of optimal prefix code that is commonly used for lossless data compression. The process of finding or using such a code proceeds by means of Huffman coding, an algorithm developed by David A. Huffman while he was a Sc.D. student at MIT, and published in the 1952 paper "A Method for the Construction of Minimum-Redundancy Codes".

The output from Huffman's algorithm can be viewed as a variable-length code table for encoding a source symbol (such as a character in a file). The algorithm derives this table from the estimated probability or frequency of occurrence (weight) for each possible value of the source symbol. As in other entropy encoding methods, more common symbols are generally represented using fewer bits than less common symbols. Huffman's method can be efficiently implemented, finding a code in time linear to the number of input weights if these weights are sorted. However, although optimal among methods encoding symbols separately, Huffman coding is not always optimal among all compression methods (some outputs from compression can end up having a larger size than the input file).

## Usage
Requires the `Bitarray` and `Pickle` Python packages.

### Encoding

Takes a text file to compress and creates a `.hc` file which is the compression of the input file using Huffman Codes

```
python3 HuffmanEncode.py input.txt
```

### Decoding 

Takes a file with the `.hc` extension (i.e. the output of an encoding from above), and creates a decompressed text file of the same name.

```
python3 HuffmanDecode.py input.hc
```