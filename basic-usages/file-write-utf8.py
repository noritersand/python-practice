import codecs

f = codecs.open("result.txt", "w", "utf-8") # w: write, r: read, a: append
# file.write(u'\ufeff')
f.write('한그을')
f.close()
