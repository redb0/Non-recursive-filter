import wave
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from document import Document
# для многопоточности
from concurrent.futures import ThreadPoolExecutor


def make_format_time(M, nframes, duration, k):

    # замыкание
    def format_time(x, pos=None):
        progress = int(x / float(nframes) * duration * k * M)
        mins, secs = divmod(progress, 60)
        hours, mins = divmod(mins, 60)
        out = "%d:%02d" % (mins, secs)
        if hours > 0:
            out = "%d:" % hours
        return out

    return format_time


def make_format_db(peak):

    def format_db(x, pos=None):
        if pos == 0:
            return ""
        if x == 0:
            return "-inf"

        db = 20 * math.log10(abs(x) / float(peak))
        return int(db)

    return format_db


# функция дискретизации
def sampling(M, nframes, nchannels, samples, k, peak, myLogger):
    nframes_discret = int(nframes / M)

    channels = []

    # построение графика
    for n in range(nchannels):
        # разбор сэмплов по каналам
        channels.append([])
        channels[n] = samples[n::nchannels]

        channels[n] = channels[n][0::int(k * M)]
        if nchannels == 1:
            channels[n] = channels[n] - peak

    myLogger("Характеристики дискретизированного сигнала")
    myLogger("Количество каналов: " + str(nchannels))
    myLogger("Коэффициент дискретизации: " + str(M))
    myLogger("Общее число семплов: " + str(nframes_discret))
    myLogger("----------------------------------")

    return channels


# функция построения графика сигнала
def print_graph(channels, num, M, nframes, duration, k, peak):

    for n in range(len(channels)):
        axes = plt.subplot(4, 1, n + 1 + num, facecolor='k')
        axes.plot(channels[n], "g")
        # axes.yaxis.set_major_formatter(ticker.FuncFormatter(make_format_db(peak)))
        plt.grid(True, color="w")
        # axes.xaxis.set_major_formatter(ticker.FuncFormatter( make_format_time(M, nframes, duration, k) ))
        plt.title("Сигнал", loc='center')
        plt.xlabel("Время")
        plt.ylabel("Амплитуда")


def print_graph_mono(samples, M, nframes, duration, k, peak):
    axes = plt.subplot(facecolor='k')
    axes.plot(samples, "g")
    axes.yaxis.set_major_formatter(ticker.FuncFormatter(make_format_db(peak)))
    plt.grid(True, color="w")
    axes.xaxis.set_major_formatter(ticker.FuncFormatter(make_format_time(M, nframes, duration, k)))
    plt.title("Сигнал", loc='center')
    plt.xlabel("Время")
    plt.ylabel("Напряжение")


# функция для преобразования Фурье
def fourier_transform(signal):
    frequencies = []

    for n in range(len(signal)):
        frequencies.append([])
        frequencies[n] = np.fft.rfft(signal[n], n=None, axis=-1)
        frequencies[n] = np.abs(frequencies[n])

    return frequencies


# функция построения частотного графика
def print_frequency_graph(channels, num, framerate):

    for n in range(len(channels)):
        axes = plt.subplot(4, 1, n + 1 + num, facecolor="k")
        plt.title("Спектр", loc='center')
        # np.arange(0., framerate / 2, (framerate / 2)/len(channels[n])),
        axes.plot(channels[n], "g")
        axes.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: x*((framerate / 2) / (len(channels[n]) + 1))))
        plt.xticks(np.arange(0, len(channels[n]) - 1, len(channels[n]) / 10))
        axes.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
        plt.grid(True, color="w")
        plt.xlabel("Частота, Гц")
        plt.ylabel("Интенсивность")


# без многопоточности
# def recovery(channels, nframes, M, myLogger):
#     nframes = int(nframes * M)
#
#     recovery_signal = []
#
#     #
#     for n in range(len(channels)):
#         channel = np.zeros((1, nframes), int)
#         for i in range(len(channels[n])):
#             for j in range(M):
#                 channel[0][i * M + j] = int(channels[n][i])
#                 # recovery_signal[n].append(int(channels[n][i]))
#         recovery_signal.append(channel[0])
#
#     myLogger("Характеристики восстановленного сигнала")
#     myLogger("Количество каналов: " + str(len(recovery_signal)))
#     myLogger("Коэффициент дискретизации: " + str(1))
#     myLogger("Общее число семплов: " + str(nframes))
#     myLogger("----------------------------------")
#
#     return recovery_signal


# функция для записи сигнала в файл
def save(recovery_signal, sampwidth, framerate, comptype, myLogger, f_to_save_in_1):
    # myLogger("Подождите, идет сохранение....")
    signal = []
    # if len(recovery_signal) != 1:
    # # совмещение сигнала из разных каналов в одном списке
    #     for i in range(len(recovery_signal[0])):
    #         for n in range(len(recovery_signal)):
    #             signal.append(recovery_signal[n][i])
    #     nframes = int(len(signal) / 2)
    # else:

    nframes = int(len(recovery_signal) / 2)

    # file_name = MainWindow.showSaveDialog()
    wf = wave.open(f_to_save_in_1, 'wb')
    # wf2 = wave.open(f_to_save_in_2, 'wb')

    # nchannels - число каналов
    # sampwidth - число байт на семпл
    # framerate - число фреймов (последовательность семплов в момент времени) в секунду
    # nframes - общее число фреймов
    # comptype - тип сжатия
    # compname - имя типа сжатия
    nchannels = 1
    # nframes = int(len(signal) / 2)

    # del recovery_signal

    compname = "nope"
    wf.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
    # wf2.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))

    try:
        # if sampwidth == 1:
        #     # преобразование в массив
        #     b = np.array(signal, dtype=np.dtype('<u1'))
        # else:
        #     b = np.array(signal, dtype=np.dtype('<i%d' % sampwidth))

        type = ['B', 'h', 'l', 'l'] # 1, 2, 3??????, 4 байта
        b = np.array(recovery_signal, dtype=np.dtype(type[sampwidth - 1]))

        del recovery_signal

        # запись байт
        wf.writeframesraw(b.tostring())
        # wf2.writeframes(b.tostring())
    except Exception as e:
        myLogger("Произошло неожиданное исключение: " + str(e))

    wf.close()
    # wf2.close()

    myLogger("----------Обработанные файлы сохранены----------")


def open_file(file_name, myLogger):

    new_doc = Document(file_name)

    # открытие файла только для чтения
    wf = wave.open(file_name, 'r')

    # считывание параметров сигнала
    # nchannels - число каналов
    # sampwidth - число байт на семпл
    # framerate - число фреймов (последовательность семплов в момент времени) в секунду
    # nframes - общее число фреймов
    # comptype - тип сжатия
    # compname - имя типа сжатия
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wf.getparams()
    myLogger("Характеристики исходного сигнала")
    myLogger("Количество каналов: " + str(nchannels))
    myLogger("Число байт на семпл: " + str(sampwidth))
    myLogger("Число семплов в секунду (частота): " + str(framerate))
    myLogger("Общее число семплов: " + str(nframes))
    myLogger("Тип сжатия: " + str(comptype))
    myLogger("Имя типа сжатия: " + str(compname))

    # пиковое значение амплитуды
    peak = 256 ** sampwidth / 2
    myLogger("Пиковое значение амплитуды: " + str(peak))
    myLogger("----------------------------------")

    # считывание и возврат не более nframes фреймов аудио как строки байтов
    data = wf.readframes(nframes)
    wf.close()

    new_doc.set_data(data)

    return (data, nchannels, sampwidth, framerate, nframes, comptype)


#
# N - порядок фильтра (количество коэффициентов)
# Fs - частота полосы пропускания
# Fx - частота полосы подавления (затухания)
# Fd - частота дискретизации
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
        h[i] = h_id[i] * w[i]

    # нормирование
    s = np.sum(h)
    for i in range(N):
        h[i] = h[i] / s

    out_signal = np.zeros((len(signal), len(signal[0])))
    for n in range(len(signal)):
        for i in range(len(signal[n])):
            out_signal[n][i] = 0
            for j in range(N - 1):
                if i - j >= 0:
                    out_signal[n][i] = out_signal[n][i] + h[j] * signal[n][i - j]

    return out_signal, h, w, Fc, h_id


def main(data, nchannels, sampwidth, framerate, comptype, N, myLogger, f_to_save_in_1, Fs, Fx):
    # имя файла с исходным треком
    # file_name = "A_Necessary_End.wav"
    # длительность отрезка сигнала  в секундах
    # обработка всего трека занимает уйму памяти, выкидывает с ошибкой
    length_signal = 60

    types = {
        1: np.int8,
        2: np.int16,
        4: np.int32
    }

    # высота и ширина графика
    w, h = 1600, 300
    DPI = 72

    # пиковое значение амплитуды
    peak = 256 ** sampwidth / 2

    # длительность потока в секундах
    duration = 44100 * length_signal / 44100
    # для всего трека
    # duration = nframes / framerate

    # разбор битов на семплы
    # fromstring - создает одномерный массив
    samples = np.fromstring(data, dtype=types[sampwidth])

    # коэффициент прореживания сигнала для построения графика
    k = 1
    # если строить только графики жрет меньше памяти
    # k = nframes / w / 32

    channels = []

    # распределение семплов по каналам
    for n in range(nchannels):
        channels.append([])
        # получение первых двух минут из трека
        sampl = samples[44100*length_signal*sampwidth:44100*(length_signal * 2)*sampwidth]
        # разбор сэмплов по каналам
        channels[n] = sampl[n::nchannels]

        # можно прорядить для построения только графиков
        # channels[n] = channels[n][0::int(k)]
        if nchannels == 1:
            channels[n] = channels[n] - peak

    del samples, sampl
    # новое количество фреймов в новом отрезке сигнала !!!!!!
    nframes = len(channels[0])

    # распределение частот исходного сигнала
    frequency_distribution_channels = fourier_transform(channels)

    # создание фигуры для рисования графиков
    plt.figure(1, figsize=(float(w) / DPI, float(h) / DPI), dpi=DPI)
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.98, top=0.98, wspace=0, hspace=0.3)

    # график исходного сигнала
    print_graph(channels, 0, N, nframes, duration, k, peak)
    # график спектра исходного сигнала
    print_frequency_graph(frequency_distribution_channels, 2, framerate)

    plt.savefig("wave", dpi=DPI)
    plt.show()

    del frequency_distribution_channels

    # настройки нерекурсивного цифрового фильтра
    # N = 20
    Fd = 44100

    (filter_signal, h_n, w_func, Fc, h_id) = filter(N, Fs, Fx, Fd, channels)

    frequency_channels = fourier_transform(filter_signal)

    del channels

    # график идеальной импульсной характеристики
    plt.figure()
    axes = plt.subplot(1, 2, 1, facecolor='k')
    axes.plot(h_id, "g")
    plt.grid(True, color="w")
    plt.title("Идеальная импульсная характеристика", loc='center')
    plt.xlabel("Частота")
    plt.ylabel("Амплитуда")

    # график импульсной характеристики
    axes = plt.subplot(1, 2, 2, facecolor='k')
    axes.plot(h_n, "g")
    plt.grid(True, color="w")
    plt.title("Импульсная характеристика фильтра (функция Блекмена)", loc='center')
    plt.xlabel("Частота")
    plt.ylabel("Амплитуда")
    plt.show()

    # график сигнала после фильтра
    plt.figure(1, figsize=(float(w) / DPI, float(h) / DPI), dpi=DPI)
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.98, top=0.98, wspace=0, hspace=0.3)
    print_graph(filter_signal, 0, N, nframes, duration, k, peak)
    print_frequency_graph(frequency_channels, 2, framerate)

    plt.savefig("wave_filter", dpi=DPI)
    plt.show()

    # запись в файл
    save(filter_signal, sampwidth, framerate, comptype, myLogger, f_to_save_in_1)

