from a import run

def loop():
    i = 0
    while True:
        print('10 min intervals')
        input()
        t = 1630829772 + 36000 + 600 * i
        run(ct=600, i_time=t)
        i += 1

if __name__ == '__main__':
    loop()

#1630825567