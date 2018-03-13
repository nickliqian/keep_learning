from OpenSSL.crypto import PKey
from OpenSSL.crypto import TYPE_RSA, FILETYPE_PEM
from OpenSSL.crypto import sign, verify
from OpenSSL.crypto import X509


pk = PKey()
pk.generate_key(TYPE_RSA, 1024)

signature = sign(pk, 'hello, world!', 'sha1')
print(signature)

x509 = X509()
x509.set_pubkey(pk)
a = verify(x509, signature, 'hello, world!', 'sha1')
print(a)


