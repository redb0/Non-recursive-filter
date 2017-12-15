import numpy as np
import matplotlib.pyplot as plt


def get_sig(A, f):
    ar = np.zeros(100)
    i = 0
    x = 0
    while i < 100:
        ar[i] = A * np.sin(2 * np.pi * f * x / 1000)
        ar[i] = ar[i] + np.sin(2 * np.pi * (f * 2) * x / 1000) + np.random.uniform(-0.2, 0.2)
        i = i + 1
        x = x + 0.1

    return ar


def filter(N, Fs, Fx, Fd, signal):
    h = np.zeros(N)  # испульсная характеристика
    h_id = np.zeros(N)  # идеальная импульсная характеристика
    w = np.zeros(N)  # весовая функция Блекмена

    # импульсная характеристика фильтра
    Fc = (Fs + Fx) / (2 * Fd)

    for i in range(N):
        if i == 0:
            h_id[i] = 2 * np.pi * Fc
        else:
            h_id[i] = np.sin(2 * i * np.pi * Fc) / (np.pi * i)
        w[i] = 0.42 - 0.5 * np.cos((2 * np.pi * i) / (N - 1)) + 0.08*np.cos((4 * np.pi * i) / (N - 1))
        # w[i] = 1
        h[i] = h_id[i] * w[i]

    # нормирование
    s = np.sum(h)
    for i in range(N):
        h[i] = h[i] / s

    out_signal = np.zeros(len(signal))
    for i in range(len(signal)):
        out_signal[i] = 0
        for j in range(N): # N - 1
            if i - j >= 0:
                out_signal[i] = out_signal[i] + h[j] * signal[i - j]

    return out_signal, h, w, Fc, h_id


# функция для преобразования Фурье
def fourier_transform(signal):
    frequencies = []
    frequencies = np.fft.rfft(signal, n=None, axis=-1)
    frequencies = np.abs(frequencies)

    return frequencies


def main_sin(N, Fs, Fx):
    A = 1
    f = 125
    signal = get_sig(A, f)
    frequencies_signal = fourier_transform(signal)

    plt.figure()
    axes = plt.subplot(1, 2, 1, facecolor='k')
    axes.plot(signal, "g")
    plt.grid(True, color="w")
    plt.title("Исходный сигнал", loc='center')
    plt.xlabel("Время")
    plt.ylabel("Амплитуда")
    # plt.show()

    # plt.figure()
    axes = plt.subplot(1, 2, 2, facecolor='k')
    axes.plot(frequencies_signal, "g")
    plt.grid(True, color="w")
    plt.title("Спектр исходного сигнала", loc='center')
    plt.xlabel("Частота")
    # plt.ylabel("Амплитуда")
    plt.show()

    Fd = 1000
    (out_signal, h, w, Fc, h_id) = filter(N, Fs, Fx, Fd, signal)
    frequencies_out_signal = fourier_transform(out_signal)

    plt.figure()
    axes = plt.subplot(1, 2, 1, facecolor='k')
    axes.plot(h_id, "g")
    plt.grid(True, color="w")
    plt.title("Идеальная импульсная характеристика", loc='center')
    plt.xlabel("Время")
    plt.ylabel("Амплитуда")
    # plt.show()

    # plt.figure()
    axes = plt.subplot(1, 2, 2, facecolor='k')
    axes.plot(h, "g")
    plt.grid(True, color="w")
    plt.title("Импульсная характеристика (окно Блекмена)", loc='center')
    plt.xlabel("Время")
    plt.ylabel("Амплитуда")
    plt.show()

    plt.figure()
    axes = plt.subplot(facecolor='k')
    axes.plot(w, "g")
    plt.grid(True, color="w")
    plt.title("Функция Блекмена", loc='center')
    # plt.xlabel("Время")
    # plt.ylabel("Амплитуда")
    plt.show()

    plt.figure()
    axes = plt.subplot(1, 2, 1, facecolor='k')
    axes.plot(out_signal, "g")
    plt.grid(True, color="w")
    plt.title("Сигнал после применения фильтра", loc='center')
    plt.xlabel("Время")
    plt.ylabel("Амплитуда")
    # plt.show()

    # plt.figure()
    axes = plt.subplot(1, 2, 2, facecolor='k')
    axes.plot(frequencies_out_signal, "g")
    plt.grid(True, color="w")
    plt.title("Спектр отфильтрованного сигнала", loc='center')
    plt.xlabel("Частота")
    # plt.ylabel("Амплитуда")
    plt.show()


if __name__ == '__main__':
    main()
