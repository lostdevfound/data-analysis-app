from flask import Flask, jsonify, request
from flask import render_template
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.palettes import Spectral11
from bokeh.resources import INLINE
from bokeh.models import ColumnDataSource, AjaxDataSource, DatetimeTickFormatter
import numpy as np
import math
import sympy as sp
import data_tech_analysis.tech_analysis as ta
import urllib.request, json
import re

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/handle_data', methods=["POST", "GET"])
def handle_data():

    # get the form value and check it
    dataOption = request.form['selectData']
    if dataOption != 'Stock' or dataOption != 'Weather' or dataOption != 'Random':
        homepage()

    timeData = []
    valueData = []

    # If the selection is Stock
    if (dataOption == 'Stock'):
        url = 'https://www.highcharts.com/samples/data/jsonp.php?filename=aapl-c.json&callback=?'
        req = urllib.request.Request(url, None,{ 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'} )

        with urllib.request.urlopen(req) as url:
            data = url.read().decode().split('\n')[1750:]

        cleanedData = []
        regex = re.compile('/\*.*\*/')

        for line in data:
            if not regex.match(line):
                cleanedData.append(line)

        cleanedData = '[' + ''.join(cleanedData)[:-2]
        cleanedData = json.loads(cleanedData)
        timeData = [datum[0] for datum in cleanedData]
        valueData = [datum[1] for datum in cleanedData]

    firstPlot = figure(title="{}".format(dataOption),plot_width=400, plot_height=200,
                       toolbar_location=None, responsive=True, x_axis_type='datetime',
                       tools="pan,wheel_zoom")
    firstPlot.line(timeData, valueData, legend="Original data", line_width=3)
    firstPlot.circle(timeData, valueData, size=7, fill_color='White',line_width=3, line_dash='solid')

    firstScript, firstDiv = components(firstPlot,INLINE)
    firstPlot.xaxis.formatter=DatetimeTickFormatter(formats=dict(
        seconds=["%d %B %Y"],
        minutes=["%d %B %Y"],
        hours=["%d %b %Y"],
        days=["%d %b %Y"],
        months=["%d %b %Y"],
        years=["%d %b %Y"]))

    # create a plot
    origPlot = figure(title="Fourier curve fitting", plot_width=400, plot_height=200, toolbar_location=None, responsive=True, tools="pan,wheel_zoom")
    origPlot.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
    origPlot.yaxis.minor_tick_line_color = None  # turn off x-axis minor ticks

    # Fourier and Original data plot
    N = 10
    series, trigTerms = ta.fourierTrigSeries(valueData, n=N)
    # Original Line
    xline = [i for i in range(len(valueData))]
    origPlot.line(xline, valueData, legend="Original data", color='green', line_width=3, line_dash='dashed')
    origPlot.circle(xline, valueData,fill_color='White', size=7, color='green', line_width=3, line_dash='solid')
    # Fourier Line
    xs = np.arange(0, len(xline), .3)
    print(len(xs))
    origPlot.line(xs, series(xs), legend="Fourier Trig Series n={}".format(N), line_width=3)
    # Legen color setup
    origPlot.legend.background_fill_color = "LightGray"
    # origPlot.legend.background_fill_alpha = 0.4
    # get script and div for the plot
    origScript, origDiv = components(origPlot,INLINE)

    # Amplitude plot
    coef, trigFuncs = zip(*trigTerms)
    trigFuncsString = [str(trigfunc) for trigfunc in trigFuncs[2:]]
    print(trigTerms)
    ampPlot = figure(title="Frequency Amp", plot_width=400, plot_height=200, toolbar_location=None, x_range=trigFuncsString, responsive=True)
    ampPlot.yaxis.minor_tick_line_color = None
    ampPlot.circle(trigFuncsString, coef[2:], line_width=3, size=6)
    ampPlot.xaxis.major_label_orientation = math.pi/4

    x0 = [i + 1 for i in range(len(coef)-2)]
    x1 = coef[2:]
    ampPlot.ray(x=0, y=0, angle=0, length=(N*2 + 2), line_width=3, line_color="purple", line_alpha=0.5)
    ampPlot.segment(x0=x0, y0=0, x1=x0, y1=coef[2:], line_width=3)
    ampScript, ampDiv = components(ampPlot, INLINE)

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
    freqScript, freqDiv = components(freqPlot, INLINE)

    return jsonify(
                   firstPlotDiv = firstDiv,
                   firstPlotScript = firstScript,
                   origPlotDiv = origDiv,
                   origPlotScript = origScript,
                   freqPlotDiv = freqDiv,
                   freqPlotScript = freqScript,
                   ampPlotDiv = ampDiv,
                   ampPlotScript = ampScript,
                   js_resources=INLINE.render_js(),
                   css_resources=INLINE.render_css()
                   )
    # return render_template('index.html', origScript=origScript, origPlot=origDiv, ampScript=ampScript, ampPlot=ampDiv, freqScript=freqScript, freqPlot=freqDiv)

@app.route('/')
def homepage():
    # create a plot
    # origPlot = figure(title="Fourier curve fitting", plot_width=400, plot_height=200, x_range=(0,14), toolbar_location=None, responsive=True)
    # origPlot.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
    # origPlot.yaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
    #
    # origScript, origDiv = components(origPlot)
    #
    # N = 15
    # xs = np.arange(0, N, 0.1)
    # data = np.random.randn(N)
    # xNumberLine = [i for i in range(len(data))]
    # series, trigTerms = ta.fourierTrigSeries(data, n=N)
    # coef, trigFuncs = zip(*trigTerms)
    # trigFuncsString = [str(trigfunc) for trigfunc in trigFuncs]
    # x0 = [i + 1 for i in range(len(coef))]
    # x1 = coef
    #
    # ampPlot = figure(title="Frequency Amp", plot_width=400, plot_height=200, toolbar_location=None, x_range=trigFuncsString,responsive=True)
    # ampPlot.yaxis.minor_tick_line_color = None
    # ampPlot.circle(trigFuncsString, coef, line_width=3, size=6)
    # ampPlot.xaxis.major_label_orientation = math.pi/4
    #
    # ampPlot.ray(x=0, y=0, angle=0, length=(N*2 + 2), line_width=3, line_color="purple", line_alpha=0.5)
    # ampPlot.segment(x0=x0, y0=0, x1=x0, y1=coef, line_width=3)
    # ampScript, ampDiv = components(ampPlot)
    #
    # # Frequency plot
    #
    # freqPlot = figure(title="Frequency decomposition", plot_width=400, plot_height=200, toolbar_location=None, responsive=True)
    #
    # x = sp.Symbol('x')
    # numLines = len(trigFuncs)
    # color_pallete = Spectral11*numLines
    #
    # funcList = []
    #
    # for i in range(numLines):
    #     if i < 2:
    #         continue
    #     f = sp.lambdify(x, trigFuncs[i], modules=['numpy'])
    #     funcList.append(coef[i]*f(xs))
    #
    # numFunc = len(funcList)
    # freqPlot.multi_line([xs]*numFunc, funcList, color=color_pallete)
    #
    # freqPlot.xaxis.minor_tick_line_color = None
    # freqPlot.yaxis.minor_tick_line_color = None
    # freqScript, freqDiv = components(freqPlot)

    return render_template('index.html',
                            # origScript=origScript,
                            # origPlot=origDiv,
                            # ampScript=ampScript,
                            # ampPlot=ampDiv,
                            # freqScript=freqScript,
                            # freqPlot=freqDiv,
                            js_resources=INLINE.render_js(),
                            css_resources=INLINE.render_css())

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
