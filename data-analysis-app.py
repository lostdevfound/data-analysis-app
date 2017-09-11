from flask import Flask, jsonify, request
from flask import render_template
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.palettes import Spectral11
from bokeh.resources import INLINE
from bokeh.models import ColumnDataSource, AjaxDataSource, DatetimeTickFormatter
import numpy as np
import pandas as pd
import math
import sympy as sp
import data_tech_analysis.tech_analysis as ta
import urllib.request, json
import re

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def homepage():
    return render_template('index.html', js_resources=INLINE.render_js(), css_resources=INLINE.render_css())


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/compute', methods=["POST", "GET"])
def compute():
    """ The method is called with the Compute button is pressed"""

    # get the form value and check it
    dataOption = request.form['selectData']
    if dataOption != 'Stock' or dataOption != 'Weather' or dataOption != 'Random':
        homepage()

    timeData, valueData = dataSelection(dataOption)
    # create a plot for the original data
    firstPlot = figure(title="{}".format(dataOption),plot_width=400, plot_height=200, responsive=True, x_axis_type='datetime')
    firstPlot.toolbar.logo = None

    firstPlot.line(timeData, valueData, legend="Original data",color='green', line_width=3)
    firstPlot.circle(timeData, valueData, size=7, fill_color='White',color='green',line_width=3, line_dash='solid')
    firstPlot.xaxis.formatter=DatetimeTickFormatter(formats=dict(
                                                                 seconds=["%d %B %Y"],
                                                                 minutes=["%d %B %Y"],
                                                                 hours=["%d %b %Y"],
                                                                 days=["%d %b %Y"],
                                                                 months=["%d %b %Y"],
                                                                 years=["%d %b %Y"]))

    firstScript, firstDiv = components(firstPlot,INLINE)

    #### Get the Fourier Analysis graph elements####
    fourierGraphs= fourierGraph(valueData, 2)
    origScript = fourierGraphs[0]
    origDiv = fourierGraphs[1]
    ampScript = fourierGraphs[2]
    ampDiv = fourierGraphs[3]
    freqScript = fourierGraphs[4]
    freqDiv =fourierGraphs[5]
    trendScript = fourierGraphs[6]
    trendDiv =fourierGraphs[7]
    return jsonify(
                   firstPlotDiv = firstDiv,
                   firstPlotScript = firstScript,
                   origPlotDiv = origDiv,
                   origPlotScript = origScript,
                   freqPlotDiv = freqDiv,
                   freqPlotScript = freqScript,
                   ampPlotDiv = ampDiv,
                   ampPlotScript = ampScript,
                   trendPlotDiv = trendDiv,
                   trendPlotScript = trendScript,
                   js_resources=INLINE.render_js(),
                   css_resources=INLINE.render_css()
                   )


@app.route('/update_fourier', methods=["POST", "GET"])
def update_fourier():
    """ The method is called when the slider is changed """

    # get the form values and check it
    dataOption = request.form['selectData']
    fourierN = int(request.form['fourierN'])
    # check the client side data
    if dataOption != 'Stock' and dataOption != 'Weather' and dataOption != 'Random':
        homepage()
    if fourierN > 40 or fourierN < 0:
        homepage()

    timeData, valueData = dataSelection(dataOption)

    #### Get the Fourier Analysis graph elements####
    fourierGraphs= fourierGraph(valueData, fourierN)
    origScript = fourierGraphs[0]
    origDiv = fourierGraphs[1]
    ampScript = fourierGraphs[2]
    ampDiv = fourierGraphs[3]
    freqScript = fourierGraphs[4]
    freqDiv =fourierGraphs[5]
    trendScript = fourierGraphs[6]
    trendDiv =fourierGraphs[7]
    return jsonify(
                   origPlotDiv = origDiv,
                   origPlotScript = origScript,
                   freqPlotDiv = freqDiv,
                   freqPlotScript = freqScript,
                   ampPlotDiv = ampDiv,
                   ampPlotScript = ampScript,
                   trendPlotDiv = trendDiv,
                   trendPlotScript = trendScript,
                   js_resources=INLINE.render_js(),
                   css_resources=INLINE.render_css()
                   )


@app.route('/update_trend', methods=["POST", "GET"])
def update_trend():

    # get the form values and check it
    dataOption = request.form['selectData']
    fourierN = int(request.form['fourierN'])
    convolutionType = request.form['type']
    convFactor = float(request.form['convolutionFactor'])

    legend = 'denoised data'

    if convolutionType == 'lowFreq':
        convFactor = convFactor / 200
        legend = 'detrended data'

    # check the client side data
    if dataOption != 'Stock' and dataOption != 'Weather' and dataOption != 'Random':
        homepage()

    if fourierN > 40 or fourierN < 0:
        homepage()

    timeData = []
    valueData = []

    timeData, valueData = dataSelection(dataOption)

    series, trigTerms = ta.fourierTrigSeries(valueData, fourierN)
    convolvedSeries, convolvedTrigTerms = ta.convolveFourierSeries(trigTerms, convFactor, convolutionType )

    x = sp.Symbol('x')
    xs = np.arange(0, len(valueData), .3)

    trendPlot = figure(title="Trend Plot",plot_width=400, plot_height=200,responsive=True)
    trendPlot.toolbar.logo = None
    trendPlot.line(xs, convolvedSeries(xs), legend= legend, line_width=3)
    trendScript, trendDiv = components(trendPlot, INLINE)

    return jsonify(trendPlotDiv=trendDiv ,
                   trendPlotScript=trendScript,
                   js_resources=INLINE.render_js(),
                   css_resources=INLINE.render_css()

    )

def fourierGraph(ivalueData=None, N=10):
    """ The computes the fourier graphs and outputs the tuple of scripts and divs """
    valueData = ivalueData
    #### Create a plot ####
    origPlot = figure(title="Fourier curve fitting", plot_width=400, plot_height=200, responsive=True)
    origPlot.toolbar.logo = None
    origPlot.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
    origPlot.yaxis.minor_tick_line_color = None  # turn off x-axis minor ticks

    # call the fourierTrigSeries() to generate lambda func series and the list of tuples trigTerms (coefs, trigFuncs)
    series, trigTerms = ta.fourierTrigSeries(valueData, n=N)
    # Original Line
    xline = [i for i in range(len(valueData))]
    origPlot.line(xline, valueData, legend="Original data", color='green', line_width=3, line_dash='dashed')
    # Fourier Line
    xs = np.arange(0, len(xline), .3)
    origPlot.line(xs, series(xs), legend="Fourier Trig Series n={}".format(N), line_width=3)
    # Legend color setup
    origPlot.legend.background_fill_color = "LightGray"

    #### Amplitude plot ####
    coef, trigFuncs = zip(*trigTerms)
    trigFuncsString = [str(trigfunc) for trigfunc in trigFuncs[2:]]
    ampPlot = figure(title="Frequency Amp", plot_width=400, plot_height=200,x_range=trigFuncsString,responsive=True)
    ampPlot.toolbar.logo = None
    ampPlot.yaxis.minor_tick_line_color = None
    ampPlot.circle(trigFuncsString, coef[2:], line_width=3, size=6)
    ampPlot.xaxis.major_label_orientation = math.pi/4
    # Create Stem graph
    x0 = [i + 1 for i in range(len(coef)-2)]
    x1 = coef[2:]
    ampPlot.ray(x=0, y=0, angle=0, length=(N*2 + 2), line_width=3, line_color="purple", line_alpha=0.5)
    ampPlot.segment(x0=x0, y0=0, x1=x0, y1=coef[2:], line_width=3)

    #### Frequency plot ####
    freqPlot = figure(title="Frequency decomposition", plot_width=400, plot_height=400, responsive=True)
    freqPlot.toolbar.logo = None
    freqPlot.xaxis.minor_tick_line_color = None
    freqPlot.yaxis.minor_tick_line_color = None


    x = sp.Symbol('x')
    numLines = len(trigFuncs)
    color_pallete = Spectral11*numLines

    for i in range(numLines):
        # ignore the first two terms as they are not trig functions but numbers
        if i < 2:
            continue
        f = sp.lambdify(x, trigFuncs[i], modules=['numpy'])
        # plot the functions
        freqPlot.line(xs,coef[i]*f(xs), color=color_pallete[i])

    #### Convolve begin #####
    trendPlot = figure(title="Trend Plot",plot_width=400, plot_height=200,responsive=True)

    trendPlot.line(xs, series(xs), line_width=3)

    origScript, origDiv = components(origPlot,INLINE)
    ampScript, ampDiv = components(ampPlot, INLINE)
    freqScript, freqDiv = components(freqPlot, INLINE)
    trendScript, trendDiv = components(trendPlot, INLINE)
    return (origScript, origDiv,ampScript, ampDiv,freqScript, freqDiv, trendScript, trendDiv)


def dataSelection(dataOption):
    # If the selection is Stock
    if dataOption == 'Stock':
        with open('data/stock.json') as json_data:
            data = json.load(json_data)
        timeData = [datum[0] for datum in data]
        valueData = [datum[1] for datum in data]

    elif dataOption == 'Weather':
        startDate = 150
        df = pd.read_csv('data/bc_weather_data.csv', parse_dates=['Date'])
        timeData = df['Date'].tolist()[startDate:]
        timeData = [datum.date() for datum in timeData]
        df = df.fillna(0)
        valueData = df['Mean Temp'].tolist()[startDate:]

    return (timeData, valueData)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
