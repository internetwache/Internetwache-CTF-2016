def change(s):
    s = s.decode('hex')
    l = len(s)
    g = list(s)
    c = '9'
    idx = 12
    q = ord(g[idx]) ^ ord(' ') ^ ord(c)
    g[idx] = chr(q)
    idx = 16
    q = ord(g[idx]) ^ ord('\t') ^ ord(c)
    g[idx] = chr(q)
    return ''.join(g).encode('hex')