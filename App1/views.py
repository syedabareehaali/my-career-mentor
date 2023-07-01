import joblib
import numpy as np

from django.contrib.auth import login
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .models import Score
from .serializers import UserSerializer, RegisterSerializer, ScoreSerializer
from knox.auth import TokenAuthentication
from django.db import transaction
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.generics import ListAPIView



class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        print("Validated")
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class ScoreCreateView(generics.CreateAPIView):
    serializer_class = ScoreSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    model_path_finalized = 'finalized_model.sav'
    model_path_medical = 'medical_model.sav'

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.model_finalized = joblib.load(self.model_path_finalized)
        self.model_medical = joblib.load(self.model_path_medical)

    def preprocessing(self, answers):
        for keys in answers:
            if keys in ['mbti-I/E-question1', 'mbti-I/E-question2', 'mbti-I/E-question3',
                        'mbti-I/E-question4', 'mbti-I/E-question5', 'mbti-I/E-question6',
                        'mbti-I/E-question7']:
                introvert += answers[keys]

            elif keys in ['mbti-S/N-question8', 'mbti-S/N-question9', 'mbti-S/N-question10',
                          'mbti-S/N-question11', 'mbti-S/N-question12', 'mbti-S/N-question13',
                          'mbti-S/N-question14']:
                sensing += answers[keys]

            elif keys in ['mbti-J/P-question15', 'mbti-J/P-question16', 'mbti-J/P-question17',
                          'mbti-J/P-question18', 'mbti-J/P-question19', 'mbti-J/P-question20',
                          'mbti-J/P-question21']:
                Judging += answers[keys]

            elif keys in ['mbti-T/F-question22', 'mbti-T/F-question23', 'mbti-T/F-question24',
                          'mbti-T/F-question25', 'mbti-T/F-question26', 'mbti-T/F-question27',
                          'mbti-T/F-question28']:
                Thinking += answers[keys]

            elif keys in ['mi-question9', 'mi-question10', 'mi-question11', 'mi-question12']:
                logical_intelligence += answers[keys]

            elif keys in ['mi-question29', 'mi-question30', 'mi-question31', 'mi-question32']:
                Nature_intelligence += answers[keys]

            elif keys in ['mi-question5', 'mi-question6', 'mi-question7', 'mi-question8']:
                Visual_intelligence += answers[keys]

            elif keys in ['mi-question21', 'mi-question22', 'mi-question23', 'mi-question24']:
                Musical_intelligence += answers[keys]

            elif keys in ['mi-question25', 'mi-question26', 'mi-question27', 'mi-question28']:
                Body_intelligence += answers[keys]

            elif keys in ['mi-question13', 'mi-question14', 'mi-question15', 'mi-question16']:
                Interpersonal_intelligence += answers[keys]

            elif keys in ['mi-question17', 'mi-question18', 'mi-question19', 'mi-question20']:
                Intrapersonal_intelligence += answers[keys]

            elif keys in ['mi-question1', 'mi-question2', 'mi-question3', 'mi-question4']:
                Verbal_intelligence += answers[keys]

            elif keys in ['mi-question33', 'mi-question34', 'mi-question35', 'mi-question36']:
                Existential_intelligence += answers[keys]

            elif (keys == 'self_question1'):
                gender = answers[keys]

            elif (keys == 'self_question2'):
                income_group = answers[keys]

        introvert = introvert/7
        sensing = sensing/7
        Judging = Judging/7
        Thinking = Thinking/7

        logical_intelligence = logical_intelligence/5
        Nature_intelligence = Nature_intelligence/5
        Visual_intelligence = Visual_intelligence/5
        Musical_intelligence = Musical_intelligence/5
        Body_intelligence = Body_intelligence/5
        Interpersonal_intelligence = Interpersonal_intelligence/5
        Intrapersonal_intelligence = Intrapersonal_intelligence/5
        Verbal_intelligence = Verbal_intelligence/5
        Existential_intelligence = Existential_intelligence/5

        preprocessed_data = {
            "gender": gender,
            "income_group": income_group,
            "sensing": sensing,
            "introvert": introvert,
            "Judging": Judging,
            "Thinking": Thinking,
            "logical_intelligence": logical_intelligence,
            "Nature_intelligence": Nature_intelligence,
            "Visual_intelligence": Visual_intelligence,
            "Musical_intelligence": Musical_intelligence,
            "Body_intelligence": Body_intelligence,
            "Interpersonal_intelligence": Interpersonal_intelligence,
            "Intrapersonal_intelligence": Intrapersonal_intelligence,
            "Verbal_intelligence": Verbal_intelligence,
            "Existential_intelligence": Existential_intelligence
        }

        return preprocessed_data

    def prediction(self, test_data):
        return 100

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        #preprocessed_data = self.preprocessing( data['answers'] )
        preprocessed_data = data

        score = self.prediction(preprocessed_data)

        # example preprocessed data for testing purpose
        preprocessed_data = {
            'user': request.user.id,
            'gender': 1,
            'income_group': 2,
            'sensing': 3.5,
            'introvert': 4.2,
            'Judging': 2.8,
            'Thinking': 3.9,
            'logical_intelligence': 4.6,
            'Nature_intelligence': 3.1,
            'Visual_intelligence': 2.7,
            'Musical_intelligence': 4.9,
            'Body_intelligence': 3.8,
            'Interpersonal_intelligence': 4.2,
            'Intrapersonal_intelligence': 2.3,
            'Verbal_intelligence': 4.1,
            'Existential_intelligence': 3.7,
            'Engineering_Field1': 'Engineering Field 1 Value',
            'Engineering_Field2': 'Engineering Field 2 Value',
            'Engineering_Field3': 'Engineering Field 3 Value',
            'Engineering_Field4': 'Engineering Field 4 Value',
            'Engineering_Field5': 'Engineering Field 5 Value',
            'Medical_Field1': 'Medical Field 1 Value',
            'Medical_Field2': 'Medical Field 2 Value',
            'Medical_Field3': 'Medical Field 3 Value',
            'score': score
        }

        serializer = self.get_serializer(data=preprocessed_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

class ScoreListView(ListAPIView):
    serializer_class = ScoreSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = Score.objects.filter(user=user)
        return queryset