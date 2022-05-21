from django.shortcuts import render


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