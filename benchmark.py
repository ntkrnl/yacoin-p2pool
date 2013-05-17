import time
start=time.time()
all=xrange(1,10**7)
def check(num):
    a=list(str(num))
    b=a[::-1]
    if a==b:
        return True
    return False
for i in all:
    if check(i):
        if check(i**2):
            print i,i**2
            
end=time.time()
print end-start
