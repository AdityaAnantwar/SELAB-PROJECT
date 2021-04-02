a = [1,2,3,4,5,6,7]
x = y = []

x = a[::3]
y = a[1::3]
z = a[2::3]
if len(a)%3 is 1:
    y.append(None)
    z.append(None)
if len(a)%3 is 2:
    z.append(None)

k = zip(x,y,z)
for p,q,r in k:
    print(p,",",q,",",r)

