import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

def plot_time_data(data,save_figure_path=None,figsize=(7, 5)):
       fig = plt.figure(figsize=figsize, dpi= 100, facecolor='w', edgecolor='k')
       # ax = plt.subplots()
       ax = plt.axes()
       ax.plot( data , linewidth = 0.6)
       plt.grid()
       plt.style.use('seaborn-whitegrid')
       ax.set(xlabel='time (s)', ylabel='sample value',
              title=f'Time domain data')
       ax.grid()
       if save_figure_path != None:
              fig.savefig(save_figure_path)
       plt.show()

def plot_fft_data(freq,data,left_part=True,xlog=True,ylog=False,figsize=(7, 5)):
       fig = plt.figure(figsize=figsize, dpi= 100, facecolor='w', edgecolor='k')
       ax = plt.axes()
       if left_part:
              freq = freq[:int(len(freq)/2)]
              data = data[:int(len(data)/2)]
       if xlog:
              plt.xscale("log")
       if ylog:
              plt.yscale("log")
       ax.grid()
       ax.grid(b=True)
       ax.plot(freq, data , linewidth = 0.6)
       ax.set(xlabel='Freq (Hz)', ylabel='Magnutude',
              title=f'Freq domain data')
       plt.show()


def plot_spectrum(spectrum,sample_name="",figsize=(5,5),origin='lower'):
    fig = plt.figure(figsize=figsize, dpi= 100, facecolor='w', edgecolor='k')
    ax = plt.axes()
    ax.set(xlabel='time', ylabel='Magnitude',
              title=f'Spectrum of a sample {sample_name}')
    ax.imshow(spectrum, interpolation='nearest', aspect='auto' , cmap='viridis',origin=origin)


def plot_fft_data_plotly(freq,data,left_part=True,xlog=True,ylog=False):
    if left_part:
              freq = freq[:int(len(freq)/2)]
              data = data[:int(len(data)/2)]
    fig = px.line(x=freq, y=data, labels={'x':'Freq (Hz)', 'y':'Magnutude'},log_x=xlog)
    fig.show()

def plot_time_data_plotly(time,data,xlog=False,ylog=False):
    fig = px.line(x=time, y=data, labels={'x':'Freq (Hz)', 'y':'Magnutude'},log_x=xlog,log_y=ylog)
    fig.show()