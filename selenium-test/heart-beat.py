import time
import threading

exec_times = 999999

def heart_beat():
    print(time.strftime('%Y-%m-%d %H:%M:%S'))

    global exec_times
    exec_times -= 1

    if exec_times > 0:
        threading.Timer(1, heart_beat).start()

heart_beat()

