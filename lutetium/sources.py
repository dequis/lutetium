import random

class RandomMeterSource:
    """A meter source that targets random values and moves 10%-30% of the way
    in each step"""

    def __init__(self, min=0, max=9000, speed_range=(0.1, 0.3)):
        self.min = min
        self.max = max
        self.speed_range = speed_range
        self.counter = 0
        self.value = (max - min) / 2 + min
        self.target = self.value
        self.speed = 0

    def step(self):
        if (self.target - self.value) < 1:
            # target reached or unset, find a new random target
            self.target = random.randint(self.min, self.max)
            self.speed = random.uniform(*self.speed_range)

        new_value = self.value + (self.target - self.value) * self.speed

        self.value = new_value

        return {
            'value': new_value,
        }

