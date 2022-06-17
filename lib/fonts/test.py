def res(x, z):
    y = (x / z)
    return y

i = 1

X = 1920
Y = int(X / 16 * 9)

arr = []
while i < 1000:
    a = res(X, i)
    b = res(Y, i)
    if  a - int(a) == 0 and b - int(b) == 0:
        arr.append((i, a, b))
    i += 1

for i in arr:
    print(i[1] / i[2])

print(arr)

