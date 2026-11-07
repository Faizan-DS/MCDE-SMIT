# Task 12 | Custom Iterable Range Toolkit  (no list, no built-in range inside)

class ReversibleRange:
    def __init__(self, start, stop, step=1):
        for value in (start, stop, step):
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError("start, stop and step must be integers")
        if step == 0:
            raise ValueError("step cannot be zero")
        self.start = start
        self.stop = stop
        self.step = step

    def __len__(self):
        if self.step > 0:
            if self.start >= self.stop:
                return 0
            return (self.stop - self.start - 1) // self.step + 1
        if self.start <= self.stop:
            return 0
        return (self.start - self.stop - 1) // (-self.step) + 1

    def __iter__(self):
        current = self.start
        while (current < self.stop) if self.step > 0 else (current > self.stop):
            yield current
            current += self.step

    def __reversed__(self):
        count = len(self)
        current = self.start + (count - 1) * self.step      # the last value
        while count > 0:
            yield current
            current -= self.step
            count -= 1

    def __contains__(self, value):
        if isinstance(value, bool) or not isinstance(value, int):
            return False
        if self.step > 0:
            inside = self.start <= value < self.stop
        else:
            inside = self.stop < value <= self.start
        return inside and (value - self.start) % self.step == 0

    def __repr__(self):
        return "ReversibleRange(" + str(self.start) + ", " + str(self.stop) + ", " + str(self.step) + ")"


if __name__ == "__main__":
    r = ReversibleRange(2, 11, 3)
    print(list(r), list(reversed(r)), len(r), 5 in r, 6 in r)  
    print(next(reversed(ReversibleRange(0, 10**12))))           