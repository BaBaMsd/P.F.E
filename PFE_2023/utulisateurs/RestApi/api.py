from rest_framework.response import Response
from utulisateurs.serializers import  PatientSerializer
from utulisateurs.models import *
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from utulisateurs.serializers import  PatientSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.decorators import api_view


#--------------login-Patient----------#

class PatientLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        
        phone = request.data['phone_number']
        password = request.data['password']
        user = User.objects.filter(phone_number=phone).first()
        patient = Patient.objects.get(nni = user.nni)
        if patient is None:
            raise AuthenticationFailed('check password')
        if user.check_password(password):
            
            refresh = RefreshToken.for_user(patient)
            return Response({
                'id':patient.id,
                'nom':patient.nom,
                'prenom':patient.prenom,
                'nni':patient.nni,
                'refresh':str(refresh),
                'access':str(refresh.access_token)
            },status=Response.status_code)
        else:
            return Response({
                             'message':'Check your credentials'
                            }, status= 401) 
            


#---------------register-Patient------------#
@api_view(['POST'])
def register_patient(request):
    nni = request.data.get('nni')

    if Patient.objects.filter(nni=nni).exists() and not User.objects.filter(nni=nni).exists():

        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 200) 
        else:
            return Response('Invalid data', status=400)
    else:
        
        return Response('ERRROR', status=400)
