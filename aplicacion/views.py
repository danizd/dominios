from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from inspect import getmembers
from pprint import pprint
import pyautogui
from django.conf import settings
from urllib.request import Request, urlopen

headers={'User-Agent': 'Mozilla/5.0'}


def formulario(request):
    form = PostForm(request.POST or None)
    dominio_limpio = '-'
    logo =  '/media/default-image.png'
    activa = '-'
    cms1 = '-'
    titulo1 = '-'
    descripcion1 = '-'
    keywords = '-'
    captura =  '/media/default-image.png'
    rrss = '-'
    infoserver = ''
    advertools_info = ''
    if form.is_valid():
        form.errors
        dominio = form.cleaned_data.get('text')
        dominio_limpio = urlparse(dominio).netloc
        logo = get_logo(dominio)
        activa = get_activa(dominio_limpio)
        cms1 = getcms(dominio)
        titulo1 = gettitle(dominio)
        descripcion1 = getdescripcion(dominio)
        keywords = getkeywords(dominio)
        captura = get_thumbnail_url(dominio)
        rrss = get_rrss(dominio)
        infoserver =   get_infoserver(dominio)
        advertools_info =   get_advertools_info(dominio)
    else:
        text = 'noooooo'
    thislist = {}
    thislist['dominio1'] = {
    'dominio' : dominio_limpio, 
    'logo' : logo,
    'activa' : activa,
    'cms' : cms1 ,
    'titulo' : titulo1 ,
    'descripcion' : descripcion1,
    'keywords' : keywords,
    'captura' : captura,
    'rrss' : rrss ,
    'infoserver' : infoserver ,
    'advertools_info' : advertools_info ,
    }
    return render(request, 'aplicacion/formulario.html', {'thislist': thislist})


def get_logo(dominio):
    import urllib.request, urllib.parse, urllib.error
    import ssl

    # --- ignore ssl certificate ---
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = Request(dominio , headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "html.parser")

    images = []
    for img in soup.findAll('img'):
        images.append(img.get('src'))
    if images :
        if 'http' in images[0] or 'https' in images[0] :
            logo = images[0]
        else:
            logo = dominio+images[0]
    else:
        logo = ''
    return logo

def get_activa(dominio):
    import requests
    url = "https://zozor54-whois-lookup-v1.p.rapidapi.com/"
    querystring = {"format":"json","domain":dominio}
    headers = {
        'x-rapidapi-host': "zozor54-whois-lookup-v1.p.rapidapi.com",
        'x-rapidapi-key': "e5dc205cc3msh8fbdc2d372e2574p1bf8bfjsn03d8d61422a7"
        }
    data = {}

    response = requests.request("GET", url, headers=headers, params=querystring)
    datos = response.json()
    for key, value in datos.items():   
        if key.lower() == 'whoisserver':        
            data['Servidor Whois'] = value

    for key, value in datos.items():   
        if key.lower() == 'rawdata':  
            ls = value[0].split("\n")
            for  val in ls:   
                data[val] = val
        #data[key] = value

    return data



def getcms(dominio):
    cms = ''
    wpLcheck = requests.get(dominio + "/wp-login.php", headers)
    if wpLcheck.status_code == 200 and "user_login" in wpLcheck.text and "404" not in wpLcheck.text:
        cms = 'Wordpress'
    wpAcheck = requests.get(dominio + "/wp-admin", headers)
    if wpAcheck.status_code == 200 and "user_login" in wpAcheck.text and "404" not in wpAcheck.text:
        cms = 'Wordpress'
    jmAcheck = requests.get(dominio + "/administrator", headers)
    if jmAcheck.status_code == 200 and "mod-login-username" in jmAcheck.text and "404" not in jmAcheck.text:
        cms = 'Joomla'
    jmScheck = requests.get(dominio, headers)
    if jmScheck.status_code == 200 and "joomla" in jmScheck.text and "404" not in jmScheck:
        cms = 'Joomla'
    drLcheck = requests.get(dominio + "/update.php", headers)

    if drLcheck.status_code == 403 and "In order to run update.php" in drLcheck.text and "404" not in drLcheck.text:
        cms = 'Drupal 8'
    elif drLcheck.status_code == 403 and "Access denied. You are not authorized to access this page" in drLcheck.text:
        cms = 'Drupal 7'

    mgRcheck = requests.get(dominio + '/RELEASE_NOTES.txt', headers)
    if mgRcheck.status_code == 200 and 'magento' in mgRcheck.text:
        cms = 'Magento'

    source = requests.get(dominio).text
    soup = BeautifulSoup(source, features="html.parser")
    content = soup.find("meta", attrs={"name":"content"})
    if content == 'blogger':
        cms = 'blogger'
    return cms
    

def gettitle(dominio):
    req = Request(dominio , headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "html.parser")
    title = soup.title.get_text()
    return title

def getdescripcion(dominio):
    req = Request(dominio , headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "html.parser")

    descripcion = soup.find("meta", attrs={"name":"description"})
    if(descripcion is not None):
        descripcion = descripcion["content"]
    else:
        descripcion ='Sin meta description'
    return descripcion

def getkeywords(dominio):
    req = Request(dominio , headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "html.parser")

    descripcion = soup.find("meta", attrs={"name":"keywords"})
    if(descripcion is not None):
        descripcion = descripcion["content"]
    else:
        descripcion ='Sin keywords'
    return descripcion

def get_thumbnail_url(dominio):
    from slugify import slugify
    from html2image import Html2Image

    source = requests.get(dominio).text
    html = BeautifulSoup(source, features="html.parser")
    hti = Html2Image(output_path='media')
    fileName = slugify(dominio).replace("-html","").replace("www-","").replace("https-","")
    output = hti.screenshot(url=str(dominio),save_as=f"{fileName}.png")
    url_image = '/media/'+fileName+'.png'
    return url_image

def get_rrss(dominio):
    rrss = []
    source = requests.get(dominio).text
    soup = BeautifulSoup(source, features="html.parser")
    for link in soup.find_all('a', href=True):
        if 'facebook.com' in link['href'] and  link['href'].split('?')[0] not in rrss:
            rrss.append(link['href'].split('?')[0])
        if 'twitter.com' in link['href'] and  link['href'].split('?')[0] not in rrss:
            rrss.append(link['href'].split('?')[0])
        if 'linkedin.com' in link['href'] and  link['href'].split('?')[0] not in rrss:
            rrss.append(link['href'].split('?')[0])
        if 'instagram.com' in link['href'] and  link['href'].split('?')[0] not in rrss:
            rrss.append(link['href'].split('?')[0])
        if 'linkedin.com' in link['href'] and  link['href'].split('?')[0] not in rrss:
            rrss.append(link['href'].split('?')[0])
        if 'youtube.com' in link['href'] and  link['href'].split('?')[0] not in rrss:
            rrss.append(link['href'].split('?')[0])
    return rrss





def get_infoserver(dominio):
    from datetime import datetime, timezone
    from http.cookiejar import http2time
    infoserver = {}
    
    headers = requests.get(dominio).headers
    # Headers is a dict so we can use items() function to get it as Key, Value.
    for key, value in headers.items():
        if key.lower() == 'date':
            key_data = 'Data de análise'
            value_data = datetime.utcfromtimestamp(http2time(value)).replace(tzinfo=timezone.utc)
        if key.lower() == 'server':
            key_data = 'Servidor'
            value_data = value
        if key.lower() in 'content-security-policy':
            key_data = 'Prevención contra ataques de Cross Site Scripting (XSS)'
            value_data = 'Sí'         
        if key.lower() in 'frame-options':
            key_data = 'Prevención contra ataques tipo Clickjacking.'
            value_data = 'Sí'    
        if key.lower() in 'content-type':
            key_data = 'Tipo de contido'
            value_data = value
        if key.lower() in 'accept-language':
            key_data = 'Idiomas aceptados'
            value_data = value
        if key.lower() in 'content-language':
            key_data = 'Idioma'
            value_data = value
        if key.lower() in 'content-length':
            key_data = 'Tamaño de portada (en bytes)'
            value_data = value
        if key.lower() in 'last-modified':
            key_data = 'Última modificación'
            value_data = datetime.utcfromtimestamp(http2time(value)).replace(tzinfo=timezone.utc)
        if key.lower() in 'x-powered-by':
            key_data = 'Tecnoloxía'
            value_data = value
        if key.lower() in 'x-generator':
            key_data = 'Tecnoloxía e versión'
            value_data = value


            
        infoserver[key_data] = value_data
       # infoserver[key] = value (trae todas as cabeceiras)

    return infoserver


def get_advertools_info(dominio):
    import sys
    import pandas as pd
    from advertools import crawl
    import json

    info = {}
    datos = {}
    key_data = ''
    value_data = ''

    crawl(dominio, 'media/dominio.jl', follow_links=False)
    with open('media/dominio.jl') as f:
        infoserver = json.loads(f.readlines()[-1])
        for key, value in infoserver.items():  
            if key.lower() in 'h1':
                key_data = 'Principal h1'
                value_data = value 
            if key.lower() in 'h2':
                key_data = 'Principal h2'
                value_data = value   
            if key.lower() in 'jsonld_logo':
                key_data = 'Logo'
                value_data = value   
            if key.lower() in 'ip_address':
                key_data = 'Dirección IP'
                value_data = value   
            if key.lower() in 'resp_headers_set-cookie':
                key_data = 'Cookie'
                value_data = value 
            if key.lower() in 'body_text':
                key_data = 'Texto de portada'
                value_data = value 
  

                
            #datos[key] = value
            if key_data != '':
                 datos[key_data] = value_data

    return datos



def post_list(request):
    thislist = {}
    thislist['dominio1'] = {
    'dominio' : 'dominio1', 
    'logo' : 'logo1' ,
    'cms' : 'cms1' ,
    'titulo' : 'titulo1' ,
    'descripcion' : 'descripcion1',
    'rrss' : 'rrss1' ,
    }
    thislist['dominio2'] = {
    'dominio' : 'dominio2', 
    'logo' : 'logo2',
    'cms' : 'cms2',
    'titulo' : 'titulo2',
    'descripcion' : 'descripcion2',
    'rrss' : 'rrss2' ,
    }
    thislist['dominio3'] = {
    'dominio' : 'dominio3', 
    'logo' : 'logo3',
    'cms' : 'cms3',
    'titulo' : 'titulo3',
    'descripcion' : 'descripcion3',
    'rrss' : 'rrss3' ,
    }
    thislist['dominio4'] = {
    'dominio' : 'dominio4', 
    'logo' : 'logo4' ,
    'cms' : 'cms4' ,
    'titulo' : 'titulo4' ,
    'descripcion' : 'descripcion4',
    'rrss' : 'rrss4' ,
    }

    return render(request, 'aplicacion/post_list.html', {'thislist': thislist})


def grafico(request):
    grafico = {}
    return render(request, 'aplicacion/grafico.html', {'grafico': grafico})


def jaja(request):
    jaja = {}
    return render(request, 'aplicacion/jaja.html', {'jaja': jaja})

