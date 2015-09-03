import binascii

if __name__ == '__main__':
    infile = 'out'
    outfile = 'out.png'
    with open(infile) as f:
        content = f.read()
    with open(outfile, 'wb') as f:
        # since reading was in text mode, we're getting endline at the end
        # which has to be removed
        f.write(binascii.unhexlify(content[:-1]))
