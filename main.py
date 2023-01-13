import time
import day25

if __name__ == '__main__':
    t0 = time.time()
    x = day25.run()
    t1 = time.time()

    dt = (t1-t0)*1000
    print()
    print('Results', x)
    print('Runtime = ', int(dt), 'msec')
    # print('Runtime = ', int(dt)/1000, 'sec')
    # print('Runtime = ', int(dt)/1000000, 'msec')

