import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO


font_size = 13
color_list = ['gray', 'turquoise', 'lightgray', 'skyblue', 'brown', 'royalblue',
			  'darkorange', 'mediumblue', 'olive', 'plum', 'lightgreen', 'deeppink']


def convert_chart_to_image():
	buffer = BytesIO()
	plt.savefig(buffer, format='png')
	plt.close()
	img   = buffer.getvalue()
	chart = base64.b64encode(img)
	chart = chart.decode('utf-8')
	buffer.close()
	return chart


def create_plotchart(x, y):
	plt.cla()
	plt.switch_backend('AGG')
	plt.figure(figsize=(10, 5))
	plt.plot(x, y, color='blue')
	plt.title('支出')
	plt.xlabel('月')
	plt.ylabel('金額')
	plt.grid(axis = 'y', color='black', linestyle = '-', linewidth = 1)
	plt.rcParams['axes.axisbelow'] = True
	plt.rcParams["font.size"] = font_size
	plt.rcParams['font.family'] = 'MS Gothic'
	chart = convert_chart_to_image()
	return chart


def create_barchart(x, y):
	plt.cla()
	plt.switch_backend('AGG')
	plt.figure(figsize=(10, 5))
	plt.bar(x, y, color=color_list)
	plt.title('月別')
	plt.xlabel('月')
	plt.xticks(rotation=45)
	plt.ylabel('金額', rotation=90)
	plt.grid(axis = 'y', color='black', linestyle = '-', linewidth = 1)
	plt.rcParams['axes.axisbelow'] = True
	plt.rcParams['figure.autolayout'] = True
	plt.rcParams["font.size"] = font_size
	plt.rcParams['font.family'] = 'MS Gothic'
	chart = convert_chart_to_image()
	return chart


def create_piechart(pie_elements, label_list):
	plt.cla()
	plt.switch_backend('AGG')
	plt.figure(figsize=(5, 5))
	plt.pie(pie_elements, labels=label_list,
		 	colors=color_list,
			startangle=90,
			counterclock=False,
			autopct="%.1f%%",
			pctdistance=0.8,
			labeldistance=1.2)
	plt.title('項目別')
	plt.rcParams["font.size"] = font_size
	plt.rcParams['font.family'] = 'MS Gothic'
	chart = convert_chart_to_image()
	plt.close()
	return chart