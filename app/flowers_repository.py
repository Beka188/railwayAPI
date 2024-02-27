from attrs import define


@define
class Flower:
    name: str
    count: int
    cost: int
    id: int = 0

    def __json__(self):
        return {"name": self.name, "count": self.count, "cost": self.cost, "id": self.id}


class FlowersRepository:
    flowers: list[Flower]
    cart: list[Flower]

    def __init__(self):
        self.flowers = [Flower("flower_1", 10, 100, 1),
                        Flower("flower_2", 5, 500, 2),
                        Flower("flower_3", 100, 100, 3)]
        self.cart = []
    # необходимые методы сюда

    def get_flowers(self):
        return self.flowers

    def __json__(self):
        return {"flowers": [Flower.__json__(flower) for flower in self.flowers]}

    def add(self, flower: Flower):
        for i in range(len(self.flowers)):
            flow = self.flowers[i]
            if flow.name == flower.name:
                flower.id = self.flowers[i].id
                self.flowers[i] = flower
                return self.flowers[i].id
        flower.id = len(self.flowers) + 1
        self.flowers.append(flower)
        return flower.id

    def add_to_cart(self, flower: Flower):
        self.cart.append(flower)

    def total_price(self):
        total = 0
        for flower in self.cart:
            total += flower.cost
        return total

    def __jsonCart__(self):
        return {"cart items": [Flower.__json__(flower) for flower in self.cart], "total_price": self.total_price()}
    # конец решения
