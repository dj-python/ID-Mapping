f = open('info.txt', 'r')
lines = f.readlines()
f.close()
c = lines[4][-3:-1]
d = lines[5][-3:-1]
e = lines[6][-5:-1]
f = lines[7][-5:-1]



print(lines)
print(c)
print(d)
print(e)
print(f)
