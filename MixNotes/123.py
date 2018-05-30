import getopt
args = '-a -b 35 -cfoo -d bar -f a1 a2'.split()
print(args)

optlist, args = getopt.getopt(args, 'abc:d:f')
print(optlist)

print(args)
