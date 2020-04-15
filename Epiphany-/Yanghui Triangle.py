n = 0
results = []

def triangles2():
    s = [1]
    while True:
        yield s
        s = s + [0]
        s = [1] + [s[i] + s[i - 1] for i in range(-n, 0)]

def triangles():
    L = [1]
    while True:
        yield L#返回当前L列表中的元素
        L = [1] + [L[i - 1] + L[i] for i in range(1, len(L))] + [1]

for t in triangles():#或者调用triangles2()
    print(t)
    results.append(t)#把每层的列表再放入results列表中

    n = n + 1#打印杨辉三角的层数
    if n == 10:
        break
