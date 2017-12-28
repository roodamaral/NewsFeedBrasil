from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import *
import json
from django.core import serializers
import requests
from bs4 import BeautifulSoup
import re
from datetime import *
import schedule
import time
# r = request.get("http://www.infomoney.com.br/")


def index(request):
	return render(request, "first_app/index.html")


def create(request):
	return true

def get_search(request):
	print Headline.objects.filter(content__icontains = request.POST['search_box']).exists()
	print Headline.objects.filter(content__icontains = request.POST['search_box'])
	if Headline.objects.filter(content__icontains = request.POST['search_box']).exists():
		data = Headline.objects.filter(content__icontains = request.POST['search_box']).order_by('-created_at')[:30]
		return HttpResponse(serializers.serialize("json", data), content_type='application/json')
	else:
		print "Not Found:", request.POST['search_box']
		return HttpResponse("Not Found")


def get_infomoney(request):
	data = Headline.objects.filter(newspaper = "Infomoney").order_by('-created_at')[:30]
	return HttpResponse(serializers.serialize("json", data), content_type='application/json')



def get_valor(request):
	data = Headline.objects.filter(newspaper = "Valor").order_by('-created_at')[:30]
	return HttpResponse(serializers.serialize("json", data), content_type='application/json')



def get_g1(request):
	data = Headline.objects.filter(newspaper = "G1").order_by('-created_at')[:30]
	return HttpResponse(serializers.serialize("json", data), content_type='application/json')

def get_estadao(request):
	data = Headline.objects.filter(newspaper = "Estadao").order_by('-created_at')[:30]
	return HttpResponse(serializers.serialize("json", data), content_type='application/json')


def get_folha(request):
	folha_newspaper = Newspaper.objects.get(id=6)
	data = [{}]
	folhaurl = "http://m.folha.uol.com.br/ultimas-noticias/"
	folhar = requests.get(folhaurl)
	folhasoup = BeautifulSoup(folhar.content)
	folhag_data = folhasoup.find_all("ul", {"class": "list-fol"})
	for item in folhag_data:
		for i in item.contents: 
			try:
				date = i.contents[3].text.encode("utf-8")
				hl = i.contents[5].text.encode("utf-8")
				data.append({'date': date, 
				'newspaper': "Folha",
				'headline': hl
				})
				if Headline.objects.filter(content = headline).exists():
					pass
				else:
					Headline.objects.create(content = headline, newspaper = folha_newspaper)
			except:
				pass
	return HttpResponse(json.dumps(data[:20]), content_type='application/json')


def get_all(request):
	data = [{}]
	infourl = "http://www.infomoney.com.br/ultimas-noticias"
	infor = requests.get(infourl)
	valorsoup = BeautifulSoup(infor.content)
	infog_data = valorsoup.find_all("div",{"class": "section-box-secondary-container-description"})
	for item in infog_data:
		date = ""
		# print item.contents[3].text.encode("utf-8")
		x = item.contents[5].text.encode("utf-8")
		y = x.split(' ')
		date += y[0][-2:]
		date += "/11/"
		date += y[2]
		date += " "
		date += y[4]
		headline = item.contents[3].text.encode("utf-8")
		data.append({'date': date, 
		'newspaper': "Infomoney",
		'headline': item.contents[3].text.encode("utf-8")
		})
		if Headline.objects.filter(content = headline).exists():
				pass
		else:
			Headline.objects.create(content = headline, newspaper = "Infomoney")
	valorurl = "http://www.valor.com.br/ultimas-noticias"
	valorr = requests.get(valorurl)
	valorsoup = BeautifulSoup(valorr.content)
	valorg_data = valorsoup.find_all("div",{"class": "group"})
	for item in valorg_data:
		date = ""
		# print item.text.encode("utf-8")
		x = item.contents[1].text.encode("utf-8")
		y = x.split(' ')
		for i in y:
			if any(j.isdigit() for j in i):
				date += i
				date += " "		
		headline = item.contents[3].text.encode("utf-8")
		data.append({'date': date, 
		'newspaper': "Valor",
		'headline': item.contents[3].text.encode("utf-8")
		})
		if Headline.objects.filter(content = headline).exists():
				pass
		else:
			Headline.objects.create(content = headline, newspaper = "Valor")
	g1url = "http://g1.globo.com/ultimas-noticias.html"
	g1r = requests.get(g1url)
	g1soup = BeautifulSoup(g1r.content)
	g1g_data = g1soup.find_all("div",{"class": "feed-post-body"})
	for item in g1g_data:
		time = datetime.now() + timedelta(hours=6)
		headlinet = item.contents[0].find_all("p", {"class":"feed-post-body-title gui-color-primary gui-color-hover"})[0].text.encode("utf-8")
		try:
			headlines = item.contents[0].find_all("p", {"class":"feed-post-body-resumo"})[0].text.encode("utf-8")
			headline = headlinet + " - " + headlines
		except:
			pass
		x = item.contents[0].find_all("span", {"class":"feed-post-datetime"})[0].text.encode("utf-8")
		y = x.split(' ')
		if y[0] == 'agora':
			date = str(time)
		elif y[2] == "horas":			 
			ago = int(y[1]) * 60
			newtime = time - timedelta(minutes=ago)
			date =  str(newtime)
		else:
			newtime = time - timedelta(minutes=int(y[1]))
			date = str(newtime)
		data.append({'date': date, 
		'newspaper': "Valor",
		'headline': headline
		})
		if Headline.objects.filter(content = headline).exists():
				pass
		else:
			Headline.objects.create(content = headline, newspaper = "G1")
	estadaourl = "http://www.estadao.com.br/ultimas"
	estadaor = requests.get(estadaourl)
	estadaosoup = BeautifulSoup(estadaor.content)
	estadaog_data = estadaosoup.find_all("section",{"class": "col-md-12 col-sm-12 col-xs-12 init item-lista"})
	for item in estadaog_data:
		date = "" 
		headline = item.contents[1].find_all("a", {"class": "link-title"})[0].text.encode("utf-8")
		headline = ' '.join(headline.split())
		x =  item.contents[1].find_all("span", {"class": "data-posts"})[0].text.encode("utf-8")
		y = x.split(' ')
		date += y[0]
		date += "/11/"
		date += y[4]
		date += " "
		date += y[6]				
		data.append({'date': date, 
		'newspaper': "Estadao",
		'headline': headline
		})
		if Headline.objects.filter(content = headline).exists():
				pass
		else:
			Headline.objects.create(content = headline, newspaper = "Estadao")
	data = Headline.objects.order_by('-created_at')[:30]
	print "Scraped!"
	return HttpResponse(serializers.serialize("json", data), content_type='application/json')

def get_todos():
	data = [{}]
	infourl = "http://www.infomoney.com.br/ultimas-noticias"
	infor = requests.get(infourl)
	valorsoup = BeautifulSoup(infor.content)
	infog_data = valorsoup.find_all("div",{"class": "section-box-secondary-container-description"})
	for item in infog_data:
		date = ""
		# print item.contents[3].text.encode("utf-8")
		x = item.contents[5].text.encode("utf-8")
		y = x.split(' ')
		date += y[0][-2:]
		date += "/11/"
		date += y[2]
		date += " "
		date += y[4]
		headline = item.contents[3].text.encode("utf-8")
		data.append({'date': date, 
		'newspaper': "Infomoney",
		'headline': item.contents[3].text.encode("utf-8")
		})
		if Headline.objects.filter(content = headline).exists():
				pass
		else:
			Headline.objects.create(content = headline, newspaper = "Infomoney")
	valorurl = "http://www.valor.com.br/ultimas-noticias"
	valorr = requests.get(valorurl)
	valorsoup = BeautifulSoup(valorr.content)
	valorg_data = valorsoup.find_all("div",{"class": "group"})
	for item in valorg_data:
		date = ""
		# print item.text.encode("utf-8")
		x = item.contents[1].text.encode("utf-8")
		y = x.split(' ')
		for i in y:
			if any(j.isdigit() for j in i):
				date += i
				date += " "		
		headline = item.contents[3].text.encode("utf-8")
		data.append({'date': date, 
		'newspaper': "Valor",
		'headline': item.contents[3].text.encode("utf-8")
		})
		if Headline.objects.filter(content = headline).exists():
				pass
		else:
			Headline.objects.create(content = headline, newspaper = "Valor")
	g1url = "http://g1.globo.com/ultimas-noticias.html"
	g1r = requests.get(g1url)
	g1soup = BeautifulSoup(g1r.content)
	g1g_data = g1soup.find_all("div",{"class": "feed-post-body"})
	for item in g1g_data:
		time = datetime.now() + timedelta(hours=6)
		headlinet = item.contents[0].find_all("p", {"class":"feed-post-body-title gui-color-primary gui-color-hover"})[0].text.encode("utf-8")
		try:
			headlines = item.contents[0].find_all("p", {"class":"feed-post-body-resumo"})[0].text.encode("utf-8")
			headline = headlinet + " - " + headlines
		except:
			pass
		x = item.contents[0].find_all("span", {"class":"feed-post-datetime"})[0].text.encode("utf-8")
		y = x.split(' ')
		if y[0] == 'agora':
			date = str(time)
		elif y[2] == "horas":			 
			ago = int(y[1]) * 60
			newtime = time - timedelta(minutes=ago)
			date =  str(newtime)
		else:
			newtime = time - timedelta(minutes=int(y[1]))
			date = str(newtime)
		data.append({'date': date, 
		'newspaper': "Valor",
		'headline': headline
		})
		if Headline.objects.filter(content = headline).exists():
				pass
		else:
			Headline.objects.create(content = headline, newspaper = "G1")
	estadaourl = "http://www.estadao.com.br/ultimas"
	estadaor = requests.get(estadaourl)
	estadaosoup = BeautifulSoup(estadaor.content)
	estadaog_data = estadaosoup.find_all("section",{"class": "col-md-12 col-sm-12 col-xs-12 init item-lista"})
	for item in estadaog_data:
		date = "" 
		headline = item.contents[1].find_all("a", {"class": "link-title"})[0].text.encode("utf-8")
		headline = ' '.join(headline.split())
		x =  item.contents[1].find_all("span", {"class": "data-posts"})[0].text.encode("utf-8")
		y = x.split(' ')
		date += y[0]
		date += "/11/"
		date += y[4]
		date += " "
		date += y[6]				
		data.append({'date': date, 
		'newspaper': "Estadao",
		'headline': headline
		})
		if Headline.objects.filter(content = headline).exists():
				pass
		else:
			Headline.objects.create(content = headline, newspaper = "Estadao")
	data = Headline.objects.order_by('-created_at')[:30]
	print "Scraped! Todo"
	return HttpResponse(serializers.serialize("json", data), content_type='application/json')


