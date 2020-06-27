f = open('200626.txt')
i = []
for line in f:
    i.append(line)
for a in range(len(i)):
    i[a] = i[a].rstrip('\n')
n = int(i[0])
x = 0
y = 0
score = []
for a in range(1, n + 1):
    for b in i[a]:
        if b == 'O':
            x += (1 + y)
            y += 1
        else:
            y = 0
    score.append(x)
    x = 0
    y = 0
print(score) # 10, 9, 6, 55, 20