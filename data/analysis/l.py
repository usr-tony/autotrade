from a import run

def loop():
    while True:
        print('observe')
        t = input('start time:')
        ct = input('ct')
        if ct == 0 or t == 0:
            run()
        else:
            run(ct=ct, i_time=t)

if __name__ == '__main__':
    loop()

