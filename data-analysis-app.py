from flask import Flask
from flask import render_template
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.palettes import Spectral11
import numpy as np
import math
import sympy as sp
import data_tech_analysis.tech_analysis as ta

app = Flask(__name__)


@app.route('/')
def homepage():
    # create a plot
    origPlot = figure(title="Fourier curve fitting", plot_width=400, plot_height=200, x_range=(0,14), toolbar_location=None, responsive=True)
    origPlot.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
    origPlot.yaxis.minor_tick_line_color = None  # turn off x-axis minor ticks

    # Fourier and Original data plot
    N = 15
    xs = np.arange(0, N, 0.1)
    data = np.random.randn(N)
    xNumberLine = [i for i in range(len(data))]
    series, trigTerms = ta.fourierTrigSeries(data, n=N)
    # Original Line
    origPlot.line(xNumberLine, data, legend="Original data", color='green', line_width=3, line_dash='dashed')
    origPlot.circle(xNumberLine, data,fill_color='White', size=7.5, color='green', line_width=4, line_dash='solid')
    # Fourier Line
    origPlot.line(xs, series(xs), legend="Fourier Trig Series", line_width=3)
    # Legen color setup
    origPlot.legend.background_fill_color = "LightGray"
    # origPlot.legend.background_fill_alpha = 0.4
    # get script and div for the plot
    origScript, origDiv = components(origPlot)

    # Amplitude plot
    coef, trigFuncs = zip(*trigTerms)
    trigFuncsString = [str(trigfunc) for trigfunc in trigFuncs]

    ampPlot = figure(title="Frequency Amp", plot_width=400, plot_height=200, toolbar_location=None, x_range=trigFuncsString, responsive=True)
    ampPlot.yaxis.minor_tick_line_color = None
    ampPlot.circle(trigFuncsString, coef, line_width=3, size=6)
    ampPlot.xaxis.major_label_orientation = math.pi/4

    x0 = [i + 1 for i in range(len(coef))]
    x1 = coef
    ampPlot.ray(x=0, y=0, angle=0, length=(N*2 + 2), line_width=3, line_color="purple", line_alpha=0.5)
    ampPlot.segment(x0=x0, y0=0, x1=x0, y1=coef, line_width=3)
    ampScript, ampDiv = components(ampPlot)

    # Frequency plot
    freqPlot = figure(title="Frequency decomposition", plot_width=400, plot_height=200, toolbar_location=None, responsive=True)

    x = sp.Symbol('x')
    numLines = len(trigFuncs)
    color_pallete = Spectral11*numLines

    funcList = []

    for i in range(numLines):
        if i < 2:
            continue
        f = sp.lambdify(x, trigFuncs[i], modules=['numpy'])
        funcList.append(coef[i]*f(xs))

    numFunc = len(funcList)
    freqPlot.multi_line([xs]*numFunc, funcList, color=color_pallete)
    freqPlot.xaxis.minor_tick_line_color = None
    freqPlot.yaxis.minor_tick_line_color = None
    freqScript, freqDiv = components(freqPlot)

    return render_template('index.html', origScript=origScript, origPlot=origDiv, ampScript=ampScript, ampPlot=ampDiv, freqScript=freqScript, freqPlot=freqDiv)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
