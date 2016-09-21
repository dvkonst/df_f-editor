import numpy as np, matplotlib.pyplot as plt

""" using coefs
def respic_template(y_peak, negcoef, pozcoef):
    def gen_respic(x_peak):
        free_rate_left = y_peak - pozcoef*x_peak
        x_left = -free_rate_left / pozcoef
        free_rate_right = y_peak - negcoef*x_peak
        x_right = -free_rate_right / pozcoef
        def
# """


def respic_template(x_peak, y_peak, dx_left, dx_right):
    num_peaks = len(x_peak)

    a_left = y_peak / dx_left
    x_left = x_peak - dx_left
    b_left = y_peak - a_left*x_peak
    a_right = -y_peak / dx_right
    x_right = x_peak + dx_right
    b_right = y_peak - a_right*x_peak
    func_left = lambda x: a_left*x + b_left
    func_right = lambda x: a_right*x + b_right


    def respike(x):
        res = np.select([np.logical_and(x_left < x, x_peak >= x), np.logical_and(x_peak < x, x_right >= x)],
                        [func_left(x), func_right(x)])

        return sum(res)

    return np.vectorize(respike)

"""
    while n < num_peaks:

        def respeak_all(x):

        n += 1

    """
ans = respic_template(np.array([12, 10, 3, 8]), 1, 1, 5)
xx = np.array(np.arange(0, 100, 0.1))
plt.plot(xx, ans(xx))
plt.show()
print()
