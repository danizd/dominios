from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from inspect import getmembers
from pprint import pprint


# Create your views here.
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

def formulario(request):
    form = PostForm(request.POST or None)
    dominio_limpio = 'vacio'
    logo = 'vacio'
    cms1 = 'vacio'
    titulo1 = 'vacio'
    descripcion1 = 'vacio'
    captura = ''
    rrss = ''
    if form.is_valid():
        form.errors
        dominio = form.cleaned_data.get('text')
        dominio_limpio = urlparse(dominio).netloc
        logo = get_logo(dominio)
        cms1 = getcms(dominio)
        titulo1 = gettitle(dominio)
        descripcion1 = getdescripcion(dominio)
        captura = get_thumbnail_url(dominio)
        rrss = get_rrss(dominio)

    else:
        text = 'noooooo'
    thislist = {}
    thislist['dominio1'] = {
    'dominio' : dominio_limpio, 
    'logo' : logo ,
    'cms' : cms1 ,
    'titulo' : titulo1 ,
    'descripcion' : descripcion1,
    'rrss' : captura ,
    'rrss' : rrss ,
    }
    return render(request, 'aplicacion/formulario.html', {'thislist': thislist})


def get_logo(dominio):
    source = requests.get(dominio).text
    soup = BeautifulSoup(source, features="html.parser")
    images = []
    for img in soup.findAll('img'):
        images.append(img.get('src'))

    if 'http' in images[0]:
        logo = images[0]
    else:
        logo = dominio+images[0]
    return logo

def getcms(dominio):
    cms = ''
    wpLcheck = requests.get(dominio + "/wp-login.php")
    if wpLcheck.status_code == 200 and "user_login" in wpLcheck.text and "404" not in wpLcheck.text:
        cms = 'Wordpress'
    wpAcheck = requests.get(dominio + "/wp-admin")
    if wpAcheck.status_code == 200 and "user_login" in wpAcheck.text and "404" not in wpAcheck.text:
        cms = 'Wordpress'
    jmAcheck = requests.get(dominio + "/administrator")
    if jmAcheck.status_code == 200 and "mod-login-username" in jmAcheck.text and "404" not in jmAcheck.text:
        cms = 'Joomla'
    jmScheck = requests.get(dominio)
    if jmScheck.status_code == 200 and "joomla" in jmScheck.text and "404" not in jmScheck:
        cms = 'Joomla'
    drLcheck = requests.get(dominio + "/update.php")

    if drLcheck.status_code == 403 and "In order to run update.php" in drLcheck.text and "404" not in drLcheck.text:
        cms = 'Drupal 8'
    elif drLcheck.status_code == 403 and "Access denied. You are not authorized to access this page" in drLcheck.text and "404" not in drLcheck.text:
        cms = 'Drupal 7'

    mgRcheck = requests.get(dominio + '/RELEASE_NOTES.txt')
    if mgRcheck.status_code == 200 and 'magento' in mgRcheck.text:
        cms = 'Magento'

    source = requests.get(dominio).text
    soup = BeautifulSoup(source, features="html.parser")
    content = soup.find("meta", attrs={"name":"content"})
    if content == 'blogger':
        cms = 'blogger'
    return cms
    

def gettitle(dominio):
    source = requests.get(dominio).text
    soup = BeautifulSoup(source, features="html.parser")
    title = soup.title.get_text()
    return title

def getdescripcion(dominio):
    source = requests.get(dominio).text
    soup = BeautifulSoup(source, features="html.parser")
    descripcion = soup.find("meta", attrs={"name":"description"})
    if(descripcion is not None):
        descripcion = descripcion["content"]
    else:
        descripcion ='Sin meta description'
    return descripcion

def get_thumbnail_url(dominio):
    thumbnail = 'https://amtega.xunta.gal//sites/w_amtega/themes/amtega/images/logo.svg'
    return thumbnail

def get_rrss(dominio):
    rrss = []
    source = requests.get(dominio).text
    soup = BeautifulSoup(source, features="html.parser")
    for link in soup.find_all('a', href=True):
        if 'facebook.com' in link['href']:
            rrss.append(link['href'])
        if 'twwiter.com' in link['href']:
            rrss.append(link['href'])
        if 'linkedin.com' in link['href']:
            rrss.append(link['href'])
        if 'instagram.com' in link['href']:
            rrss.append(link['href'])
    return rrss
