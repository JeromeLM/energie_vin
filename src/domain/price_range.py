from dataclasses import dataclass


@dataclass
class PriceRange:
    min: float = 0.0
    max: float = None

    def is_price_within(self, price: float):
        if self.max is not None:
            return price >= self.min and price <= self.max
        return price >= self.min
