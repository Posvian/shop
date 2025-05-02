import threading
from threading import Thread, Lock, Event
import time

# 1: Суммирование чисел с блокировкой (Lock):
# Есть массив чисел(100 элементов).
# Несколько потоков(5) одновременно суммируют его элементы.
# Нужно использовать Lock, чтобы получить корректный результат при конкурентной записи.

my_array = [x for x in range(1, 101)]

print(my_array)
print(sum(my_array))

counter = 0


def thread_sum(array: list, lock: Lock):
    global counter
    while array:
        lock.acquire()
        element = array.pop()
        counter += element
        lock.release()


lock = Lock()

workers = [
    Thread(
        target=thread_sum,
        args=(
            my_array,
            lock,
        ),
    )
    for _ in range(5)
]

for worker in workers:
    worker.start()


print(counter)

# Один поток подготавливает данные (например, парсит сайт или загружает файл),
# а другие(3) — ждут, пока он закончит. Используй .wait() и .set() для координации потоков.

event = Event()


def parsing_site(event):
    print("Start parsing")
    time.sleep(5)
    print("Data ready")
    event.set()


def worker(event, worker_id):
    print(f"поток {worker_id} ожидает завершения процесса парсинга")
    event.wait()
    print(f"Поток {worker_id} начал обработку данных")


workers = [Thread(target=worker, args=(event, i)) for i in range(1, 4)]
for worker in workers:
    worker.start()

parser_thread = Thread(target=parsing_site, args=(event,))
parser_thread.start()

parser_thread.join()
for worker in workers:
    worker.join()


print("Все потоки закончили выполнение")

# 3 Модель производства и потребления (Producer-Consumer)
# Один поток (Producer) кладёт элементы в очередь,
# несколько других (Consumers) забирают и обрабатывают.
# Использовать Lock и Queue. Задача синхронизировать несколько потоков при доступе к общей структуре данных.
from queue import Queue, Empty


my_queue = Queue()
lock = Lock()


def producer(queue: Queue):
    for i in range(1, 10):
        print(f"Producer кладет элемент {i} в очередь")
        queue.put(i)
        time.sleep(1)


def consumer(queue: Queue, thread_id: int):
    while True:
        try:
            with lock:
                item = queue.get()
        except Empty:
            continue
        else:
            print(f"Поток {thread_id} обрабатывает элемент {item}")
            time.sleep(4)
            queue.task_done()
            if queue.empty():
                break


produser_thread = Thread(target=producer, args=(my_queue,))
print(f"Producer начинает работу")
produser_thread.start()


consumer_threads = [
    Thread(
        target=consumer,
        args=(
            my_queue,
            i,
        ),
        daemon=True,
    )
    for i in range(1, 4)
]
for thread in consumer_threads:
    thread.start()

parser_thread.join()

for thread in consumer_threads:
    thread.join()

my_queue.join()

print("Потоки задания 3 завершили работу")


# 4 Параллельная загрузка и ожидание завершения (join)
# Запустить 5 потоков, каждый загружает разные части большого файла (или имитирует работу time.sleep()).
# Главный поток должен дождаться завершения всех с помощью .join().

print(f"Maing Thread start")
time.sleep(3)


def loader(thread_id):
    print(f"Loader {thread_id} start loading")
    time.sleep(3)
    print(f"Loader {thread_id} finish loading")


loaders = [Thread(target=loader, args=(i,)) for i in range(1, 6)]
for loader in loaders:
    loader.start()
    loader.join()

print("Main thread finish work")
