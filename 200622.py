def F2(n):
    if(n == 1 or n == 0):
        return n
    else:
        return (F2(n - 1) + F2(n - 2))

print(F2(4)) # 3