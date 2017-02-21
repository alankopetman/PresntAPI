from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, list_route, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import detail_route
from rest_framework import mixins
from django.contrib.auth.models import User, Group
from django.views.generic import RedirectView
from django.core import serializers
from django.shortcuts import render
from serializers import CourseSerializer

