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


class AbsurdPolynomialFitSource:
    """A PV data source that pretends this is a data science problem.

    Uses data extracted from the PDF using WebPlotDigitizer[1] (data set
    available at `data/pv_curve_pdf.json`), then fits that data into a cubic
    polynomial using numpy, excluding source data points under a threshold of
    y=0.1 so the curve doesn't have to deal with the flat night portion. Then,
    when evaluating the polynomial, it uses max(0, x) to skip the negative part
    of the resulting curve.

    To avoid the numpy dependency at runtime, the generated polynomial is just
    a constant and evaluated with a list comprehension. The code to generate it
    is available below, but not executed.

    [1]: https://apps.automeris.io/wpd/
    """

    ABSURD_POLYNOMIAL = [
        -2.2971346028469987e-08,
        3.553281623353355e-05,
        -0.009035967954105878,
        -0.708485804460113
    ]

    def evaluate(self, x):
        """Evaluates polynomial at point x, equivalent to calling numpy.poly1d
        but without numpy"""

        p = self.ABSURD_POLYNOMIAL
        return sum([a * x ** i for (i, a) in enumerate(p[::-1])])

    def step(self, x):
        return max(0, self.evaluate(x))

    def make_absurd_polynomial(self, plot=False):
        """Code used to create the polynomial above.

        Not actually used at runtime, since it depends on numpy and matplotlib,
        which aren't used elsewhere."""

        import json
        import numpy

        data = json.load(open('data/pv_curve_pdf.json'))
        x = numpy.array([a[0] for a in data if a[1] > 0.1])
        y = numpy.array([a[1] for a in data if a[1] > 0.1])
        z = numpy.polyfit(x, y, 3)

        if plot:
            import matplotlib.pyplot as plt

            xp = numpy.linspace(0, 1400, 100)
            p = numpy.poly1d(z)
            _  = plt.plot(x, y, '.', xp, p(xp), '-')
            plt.ylim(0, 3.5)
            plt.show()

        return z

class NoisyAbsurdPolynomialFitSource(AbsurdPolynomialFitSource):
    """Adds a bit of random noise over AbsurdPolynomialFitSource"""

    def step(self, x):
        x += random.uniform(-1, 1)
        y = super().step(x)
        y += y * random.uniform(-0.01, 0.01)
        return max(0, y)
