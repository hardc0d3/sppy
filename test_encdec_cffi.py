from encdec_cffi import EncoderDecoder as ED

ed = ED()

c = ed.enc_str("some very long string")

print c


print ed.dec_str(c)

