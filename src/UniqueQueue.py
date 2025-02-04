from django.db.models import F
from mainapp.models import Product, ProductQueue


class UniqueQueue:
    FIFO = "FIFO"
    LIFO = "LIFO"
    STRATEGIES = [FIFO, LIFO]
    PRIORITY = [1, 2, 3]

    def __init__(self, strategy=FIFO):
        if strategy not in self.STRATEGIES:
            raise TypeError
        self.strategy = strategy
        # self.queue = ProductQueue()

    def make_stock_balance_into_sales_count(self, product: Product):
        product.stock_balance = F("stock_balance") - 1
        product.sales_count = F("sales_count") + 1
        product.save()

    def add_element(self, element: Product = None, priority=1):
        if priority not in self.PRIORITY:
            raise ValueError
        if element:
            if element.stock_balance > 0:
                try:
                    product = ProductQueue.objects.get(product_id=element.id)
                except ProductQueue.DoesNotExist:
                    self.make_stock_balance_into_sales_count(element)
                    product = ProductQueue.objects.create(
                        product=element, priority=priority
                    )

                return product

    def bulk_add_elements(self):
        pass

    def add_elements(self, products: list[Product], priorities: list[dict]):
        if products:
            for product in products:
                if product.stock_balance > 0:
                    product_priority = 1
                    for priority in priorities:
                        if priority["id"] == product.id:
                            product_priority = priority["priority"]
                    self.make_stock_balance_into_sales_count(product)
                    self.add_element(
                        element=product, priority=product_priority
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
