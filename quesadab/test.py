def gcd(m, n, count=1):
    if m%n == 0:
        return(count)
    else:
        return gcd(n, m%n, count+1)

for i in range(1, 10):
    for r in range(1, 10):
        print i, r
        print gcd(i, r)