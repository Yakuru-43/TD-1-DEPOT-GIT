from django.http import HttpResponse
from django.template import loader
import json
from django.db import connection
from django.shortcuts import render
from django.http import JsonResponse
from charts.models import Person , History , Test , Active_races
from django.views.decorators.csrf import csrf_exempt
from Crypto.Cipher import AES
from base64 import b64decode
from django.contrib.auth import authenticate , logout , login
from django.contrib.auth.decorators import login_required , permission_required

#from elasticsearch import Elasticsearch


#Authentification coté App Web
def webAppAuth(request) :
    compte = ''
    mdp =''
    if request.method == 'POST':
        compte = request.POST.get('compte')
        mdp = request.POST.get('mdp')
    compteNormalise = compte.lower()
    user = authenticate(username=compteNormalise, password=mdp)
    if user is not None:

        #L'utilisateur existe on le renvoie vers la page index
        login(request, user)
        data_set = {}
        liste = list(Active_races.objects.all())
        data_json = json.dumps(data_set)
        context ={  'data_set' : data_json,
                    'per' : liste ,
                     }
        return render(request,'charts/index.html',context)
    else :

        context = {
        'error' : 1,
         }
        return render(request, 'charts/auth-signin.html', context)

#Enregistrer les données envoyé par l'app mobile
@csrf_exempt
def test(request):

    received_json_data=json.loads(request.body)

    # code de Nabilito :
    #client.bulk(client, received_json_data, index=index)

    print(received_json_data)
    if request.method == 'POST':

        id_u = received_json_data['id_user']
        id_u = int(id_u)

        vit = received_json_data['vitesse']
        vit = float(vit)

        lat = float(received_json_data['latitude'])


        lon = float(received_json_data['longitude'])


        dist = float(received_json_data['distance'])

        haut =float(received_json_data['hauteur'])

        timestamp = received_json_data['timestamp']



    p1 = Test(id_user=id_u, vitesse=vit, latitude=lat, longitude=lon, distance=dist, hauteur=haut, app_time=timestamp)
    p1.save()
    #Formatage de la réponse pour l'app
    response = HttpResponse()
    response.status_code = 200
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = True
    response.headers["Access-Control-Allow-Headers"] = "Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response