import threading

def coder(number: int):
    print(f'Coders:  {number}')
    return

threads = []
for k in range(5):
    t = threading.Thread(target=coder, args=(k,))
    threads.append(t)
    t.start()