import os
import pandas as pd
root = None
local = None



class Directory:
    def __init__(self, path):
        self.path = path
        os.makedirs(self.path, exist_ok=True)
        self.children = {}
        self.load_folders(self.path)

    def __getitem__(self, item):
        return self.children[item]

    def __getattr__(self, item):
        return self.children[item]

    def __setitem__(self, key, path):
        self.children[key] = os.path.join(self.path, path)
        os.makedirs(self.children[key], exist_ok=True)

    def __repr__(self):
        return self.path

    def list(self):
        return list(self.children.keys())

    def dirs(self):
        return list(self.children.values())

    def load_folders(self, path):
        for folder in os.listdir(path):
            if os.path.isdir(os.path.join(path, folder)) and not folder.startswith('.'):
                print(folder, end = "\r")
                self.children[folder] = os.path.join(path, folder)
                self.load_folders(os.path.join(path, folder))


def set_root(path):
    global root
    root = Directory(path)
    print(" # Root set to: {}".format(os.path.abspath(root.path)))

def set_local(path):
    global local
    local = Directory(path)
    print(" # Local set to: {}".format(os.path.abspath(local.path)))



class Variable:
    def __init__(self):
        self.vars= {}

    def __getitem__(self, item):
        return self.vars[item]

    def __setitem__(self, key, value):
        self.vars[key] = value

    def __contains__(self, item):
        return item in list(self.vars.keys())

    def __getattr__(self, item):
        return self.vars[item]

    def __repr__(self):
        return str(list(self.vars.keys()))

    def copy(self):
        return self.vars.copy()

    def keys(self):
        return list(self.vars.keys())

    def items(self):
        return self.vars.items()

    def values(self):
        return list(self.vars.values())


vars = Variable()

