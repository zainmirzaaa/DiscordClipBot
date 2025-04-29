import queue, threading

job_queue = queue.Queue()

def worker():
    while True:
        fn, args = job_queue.get()
        try:
            fn(*args)
        finally:
            job_queue.task_done()

threading.Thread(target=worker, daemon=True).start()

def enqueue(fn, *args):
    job_queue.put((fn, args))
