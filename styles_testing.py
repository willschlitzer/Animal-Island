import matplotlib.pyplot as plt
import random
days = []
prices = []

plt.style.use('fivethirtyeight')

for i in range(365):
    days.append(i)
    if prices == []:
        prices.append(round(random.uniform(15, 45),2))
    else:
        new_price = prices[-1] + random.uniform(-5, 5)
        prices.append(round(new_price, 2))

plt.plot(days, prices)

plt.show()