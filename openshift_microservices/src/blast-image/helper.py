import binascii

if __name__ == '__main__':
    infile = 'out'
    outfile = 'out.txt'
    with open(infile) as f:
        content = f.read()
    with open(outfile, 'wb') as f:
        # since reading was in text mode, we're getting endline at the end
        # which has to be removed
        data = binascii.unhexlify(content[:-1])
        data = binascii.b2a_base64(data)
        # data = binascii.hexlify(content)
        f.write(data)
