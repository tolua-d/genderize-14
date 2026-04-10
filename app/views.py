import json

import requests
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from requests import HTTPError


# Create your views here.

class GenderizedViewSet(viewsets.ViewSet):    
    def get_gender_classified_name(self, request):
        '''calls the genderized API and returns a structured custom reponse'''

        name: str = request.GET.get('name', None)
        # check for missing or empty name parameter
        if not name or name.strip() == '':
            return Response({
                'status': 'error',
                'message': "Missing 'name' parameter"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # check for non-string name paramter
        if not name.replace(' ', '').isalpha():
            return Response({
                'status': 'error',
                'message': "'name' must only contain alphabets"
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        url = f'https://api.genderize.io?name={name}'

        response = requests.get(url)
        try:
            response.raise_for_status()
        except HTTPError:
            error_msg = json.loads(response.text)
            return Response({
                'status': 'error',
                'message': error_msg.get('error')
            }, status=response.status_code)
        
        data = response.json()

        gender = data.get('gender')
        probability = data.get('probability')        
        count = data.get('count')

        # check if gender is null or sample size is 0
        if count == 0 or gender == None:
            return Response({
                'status': 'error',
                'message': 'No prediction available for the provided name',
            }, status=status.HTTP_200_OK)
        
        # check edge case where confidence level == True 
        if (probability >= 0.7) and (count >= 100):
            is_confident = True
        else:
            is_confident = False

        processed_at = timezone.now().isoformat().replace('+00:00', 'Z')

        # renaming count to sample size
        sample_size = count

        data = {
            'name': data.get('name'),
            'gender': data.get('gender'),
            'probability': probability,
            'sample_size': sample_size,
            'is_confident': is_confident,
            'processed_at': processed_at
        }

        return Response({
            'status': 'success',
            'data': data
        }, status=status.HTTP_200_OK)