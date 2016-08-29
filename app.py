from flask import Flask, render_template, request, redirect
from bokeh.embed import components
from bokeh.plotting import figure
import simplejson as json
import pandas as pd
import requests
import numpy as np


app = Flask(__name__)

app.vars={}

def datetime(x):
	return np.array(x, dtype=np.datetime64)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html')

	else:
		app.vars['ticker'] = request.form['ticker'].upper()
		return redirect('/graph')

@app.route('/graph', methods=['GET'])
def graph():
	#Data into Pandas
	qurl = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json?column_index=4&start_date=2016-08-01&api_key=PbjyCkG1dayVcyLQx-si' % app.vars['ticker']
	r = requests.get(qurl)
	col = r.json()['dataset']['column_names']
	data = r.json()['dataset']['data']
	df = pd.DataFrame(data, columns=col)

	#Bokeh plot
	p = figure(x_axis_type="datetime", title="August 2016 Closing")
	p.grid.grid_line_alpha=0.3
	p.xaxis.axis_label = 'Date'
	p.yaxis.axis_label = 'Closing Price'
	p.line(datetime(df['Date']), df['Close'], color='#33A02C')

	script, div = components(p)

	return render_template('graph.html',ticker=app.vars['ticker'], script=script, div=div)

@app.errorhandler(500)
def error_handler(e):
	return redirect('/error')

@app.route('/error')
def error():
	return render_template('error-quandle.html',ticker=app.vars['ticker'])
	

if __name__ == '__main__':
  app.run(port=33507)
