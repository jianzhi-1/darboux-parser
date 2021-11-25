import re

### BNF
### Maybe can convert to tree form? or higher order function form?

### extra: add in regular expression
### visualize out the tree (figure out the cs61a function)

### stack can consist of characters, functions (every symbol is a function)

def split(string):
    # split string based on symbols, chars
    return []

def match(string, stack):
    # see if string matches stack
    # returns true if does, false if no
    if string == "" and stack.isEmpty():
        return True
    elif string == "":
        return False
    return True

def test():
    # ((())) symmetric
    # ()()((())) balanced
    return True

def main():
    # handles input
    while True:
        c = input()

if __name__ == "__main__":
    main()