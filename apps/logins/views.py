# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from models import User

def checkLogin(session):
  if not 'id' in session:
    return False
  return True


def index(req):
  if checkLogin(req.session):
    return redirect('/success')
  else:
    return render(req, 'logins/index.html')

def add(req):
  errors = User.objects.validateRegister(req.POST)
  if len(errors):
    for tag, error in errors.iteritems():
      messages.error(req, error, extra_tags=tag)
    return redirect('/')
  else:
    return redirect('/success')

def login(req):
  errors = User.objects.validateLogin(req.POST)
  if len(errors):
    for tag, error in errors.iteritems():
      messages.error(req, error, extra_tags=tag)
    return redirect('/')
  else:
    b = User.objects.get(email = req.POST['email'])
    req.session['id'] = b.id
    return redirect('/success')

def success(req):
  if checkLogin(req.session):
    context ={'user': User.objects.get(id = req.session['id'])}
    return render(req, 'logins/success.html',context)
  else:
    return redirect('/')

def logout(req):
  del req.session['id']
  return redirect('/')

