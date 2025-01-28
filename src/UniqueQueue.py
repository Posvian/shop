from django.db.models import F
from mainapp.models import Product, ProductQueue


class UniqueQueue:
    FIFO = "FIFO"
    LIFO = "LIFO"
    STRATEGIES = [FIFO, LIFO]

    def __init__(self, strategy=FIFO):
        if strategy not in self.STRATEGIES:
            raise TypeError
        self.strategy = strategy
        # self.queue = ProductQueue()

    def make_stock_balance_into_sales_count(self, product: Product):
        product.stock_balance = F("stock_balance") - 1
        product.sales_count = F("sales_count") + 1
        product.save()

    def add_element(self, element: Product, *args: Product, priority=1):
        if priority not in [1, 2, 3]:
            raise ValueError
        if element.stock_balance > 0:
            try:
                self.make_stock_balance_into_sales_count(element)
                ProductQueue.objects.get(product_id=element.id)
            except ProductQueue.DoesNotExist:
                ProductQueue.objects.create(product=element, priority=priority)
            else:
                return "Продукт уже в очереди"
        if args:
            for arg in args:
                if arg.stock_balance > 0:
                    self.make_stock_balance_into_sales_count(arg)
                    ProductQueue.objects.get_or_create(
                        product=arg, priority=priority
                    )

    def take_element(self):
        if len(ProductQueue.objects.all()) == 0:
            raise NotImplementedError
        if self.strategy == "LIFO":
            # value = self.queue.pop()
            value = (
                ProductQueue.objects.all().order_by("-priority", "-id").first()
            )
        else:
            # value = self.queue.pop(0)
            value = (
                ProductQueue.objects.all().order_by("-priority", "id").first()
            )
        result = Product.objects.get(id=value.product_id)
        value.delete()
        return result

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
