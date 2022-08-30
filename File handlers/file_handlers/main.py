import binascii
import codecs
import os
from xml.etree.ElementTree import ElementTree


class GenericFile:
    def get_path(self):
        return NotImplementedError("get_path() nu este implementata")

    def get_freq(self):
        return NotImplementedError("get_freq() nu este implementata")


class TextASCII(GenericFile):
    path_absolut: str
    freq = {}

    def __init__(self, path):
        self.path_absolut = path
        try:
            folder = open(self.path_absolut, 'r')
            text = folder.read()
            for c in text:
                if c in self.freq.keys():
                    self.freq[c] += 1
                else:
                    self.freq[c] = 1
        except:
            print("Eroare la citire ascii")
            pass

    def get_path(self):
        return self.path_absolut

    def get_freq(self):
        return self.freq


class XMLFile(TextASCII):
    def __init__(self, path_absolut, first_tag):
        super().__init__(path_absolut)
        self.first_tag = first_tag

    def get_first_tag(self):
        return self.first_tag


class TextUNICODE(GenericFile):
    path_absolut: str
    freq = {}

    def __init__(self, path):
        self.path_absolut = path
        try:
            folder = codecs.open(self.path_absolut, 'r')
            # folder.decode('utf-16','strict')
            text = folder.read()
            for c in text:
                if chr(c) in self.freq.keys():
                    self.freq[c] += 1
                else:
                    self.freq[c] = 1
        except:
            print("Eroare la citire UNICODE")
            pass

    def get_path(self):
        return self.path_absolut

    def get_freq(self):
        return self.freq


class Binary(GenericFile):
    path_absolut: str
    freq = {}

    def __init__(self, path):
        self.path_absolut = path
        try:
            folder = codecs.open(self.path_absolut, 'rb')
            text = folder.read()
            ascii_text = binascii.b2a_uu(text)
            for c in ascii_text:
                if c in self.freq.keys():
                    self.freq[c] += 1
                else:
                    self.freq[c] = 1
        except:
            print("Eroare la citire Binary")
            pass

    def get_path(self):
        return self.path_absolut

    def get_freq(self):
        return self.freq


class BMP(Binary):
    def __init__(self, path_absolut, width, height, bpp):
        super().__init__(path_absolut)
        self.width = width
        self.height = height
        self.bpp = bpp

    def show_info(self):
        print(" Height: " + self.height + " Width: " + self.width + " Bpp: " + self.bpp)


def testASCII(path):
    aux = 1
    try:
        new_file = open(path, 'r')
        text = new_file.read()
        size = len(text)
        a = TextASCII(path)
        freq = a.get_freq()
        nr_simboluri = len(freq.keys())
        medie = size / nr_simboluri

        high_freq = [9, 10, 13]
        for i in range(32, 129):
            high_freq += [i]

        low_freq = []
        for i in range(0, 9):
            low_freq += [i]
        low_freq += [11, 12]
        for i in range(14, 32):
            low_freq += [i]
        for i in range(128, 256):
            low_freq += [i]

        for c in high_freq:
            if chr(c) in freq.keys():
                if freq(chr(c)) < medie:
                    aux = 0

        for c in low_freq:
            if chr(c) in freq.keys():
                if freq[chr(c)] > medie:
                    aux = 0

        if aux == 1:
            return 1
        else:
            return 0
    except:
        return 0


if __name__ == '__main__':
    xml = []

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    for root, subdirs, files in os.walk(ROOT_DIR):
        for file in os.listdir(root):
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                if testASCII(file_path):
                    try:
                        tree = ElementTree.parse(file_path)
                        tree_root = tree.getroot()
                        tree_tag = tree_root.tag
                        xml_file = XMLFile(file_path, tree_tag)
                        xml.append(xml_file)
                    except:
                        pass
    for file in xml:
        print(file.get_path() + " cu tag-ul " + file.get_first_tag())
