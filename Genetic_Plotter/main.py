#https://www.youtube.com/watch?v=ZmYPzESC5YY&list=PLQVvvaa0QuDfefDfXb9Yf0la1fPDKluPF&index=16
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import style
import sys

def draw():
	style.use('fivethirtyeight')
	font = {'family': 'Verdana',
	        'weight': 'normal'}
	rc('font', **font)
	gen = []
	gBest = []
	gWorth = []
	gAverage = []
	file = open("D://Python//Genetic_Plotter//logfile.txt", "r")
	for line in file:
	        words = line.split(sep=" ")
	        if len(words) > 0:
	                gen.append(float(words[0]))
	                gBest.append(float(words[1]))
	                gWorth.append(float(words[2]))
	                gAverage.append(float(words[3]))


	plt.plot(gen, gBest)
	plt.plot(gen, gWorth)
	plt.plot(gen, gAverage)

	plt.xlabel("Поколение")
	plt.ylabel("Дистанция")
	plt.subplots_adjust(bottom=0.1,top=0.9, left=0.1)

	plt.savefig("D://Python//Genetic_Plotter//graph.png")

if __name__ == "__main__":
	draw()