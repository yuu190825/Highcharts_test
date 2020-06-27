f2 = open('out.txt', 'w')
for a in range(2):
    f1 = open(f'./in{str(a+1)}.txt')
    i = []
    for line in f1:
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
    for a in range(len(score)):
        f2.write(str(score[a]) + '\n')
    f2.write('\n')
f1.close
f2.close