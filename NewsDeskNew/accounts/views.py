from django.shortcuts import render
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.views.generic import ListView
from rest_framework.reverse import reverse_lazy
from django.db.utils import IntegrityError
from desk.models import Post, Comment, Image, Video, User
from desk.utils import conf_code_generator, conf_code_verificator, confirmation_code_sender, postman
from desk.mixins import *
# Create your views here.
