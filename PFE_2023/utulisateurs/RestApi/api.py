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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


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
    phone_number = request.data['phone_number']

    if Patient.objects.filter(nni=nni).exists() and not User.objects.filter(nni=nni).exists() and not User.objects.filter(phone_number=phone_number).exists():

        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 200) 
        else:
            return Response('Invalid data', status=400)
    else:
        
        return Response('ERRROR', status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserData(request,id):
    if request.method == 'GET':
        try:
            patient = Patient.objects.get(id=id)
            vaccination = Vaccination.objects.get(patient=patient)
        except Patient.DoesNotExist:
            return Response(status=404)
        user_data = {
        'id': vaccination.patient.id,
        'nni': vaccination.patient.nni,
        'nom_vaccination':vaccination.vaccine.nom,
        'centre':vaccination.center.nom,
        'dose_number':vaccination.dose_number,
        'dose_administré':vaccination.dose_administré,
        'date_dernier_dose':vaccination.date_darnier_dose,
        'status':vaccination.status,
        'wilaya':str(vaccination.center.moughataa.nom),
        'moughataa': str(vaccination.center.moughataa.wilaya.nom),
        }
        return Response(user_data,status = 200)

