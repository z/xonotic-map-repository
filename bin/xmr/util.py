def replace_last(s, old, new):
    return s[::-1].replace(old[::-1], new[::-1], 1)[::-1]