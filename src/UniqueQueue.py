class UniqueQueue:
    FIFO = "FIFO"
    LIFO = "LIFO"
    STRATEGIES = [FIFO, LIFO]

    def __init__(self, strategy=FIFO):
        if strategy not in self.STRATEGIES:
            raise TypeError
        self.strategy = strategy
        # self.queue = ProductQueue()

    def add_element(self, element):
        if element not in self.queue:
            self.queue.append(element)

    def take_element(self):
        value = None
        if self.queue:
            if self.strategy == "LIFO":
                value = self.queue.pop()
            else:
                value = self.queue.pop(0)
        return value

    def queue_length(self):
        return len(self.queue)


if __name__ == "__main__":
    q = UniqueQueue()
    print(q.queue_length())
    q.add_element("a")
    q.add_element("b")
    q.add_element("b")
    print(q.queue_length())
    print(q)
    print(q.take_element())
