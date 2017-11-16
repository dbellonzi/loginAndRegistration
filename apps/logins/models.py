# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)
def hasUpperAndNumber(inputString):
    hasNum = False
    hasUpper = False
    for char in inputString:
        if char.isupper():
            hasUpper=True
        elif char.isdigit():
            hasNum =True
    if hasNum and hasUpper:
        return True
    else:
        return False

class UserManager(models.Manager):
    def validateRegister(self, postData):
        errors={} 
        a = User.objects.filter(email = postData['email'])
        if a:
            errors['emailHere']=' Email already exists'
        if len(postData['fName'])<2: 
            errors['fName'] = "Your First Name Is too Short"
        if len(postData['lName'])<2:
            errors['lName'] = "Your Last Name is too short"
        if hasNumbers(postData['fName']) or hasNumbers(postData['lName']):
            errors['numInName'] = "Your first or last name has a Number in it. That is not allowed"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "This is not a valid email"
        
        if not hasUpperAndNumber(postData['pasw']):
            errors['noUpperorNum']= "Your password has no Upper case or a number."
        if postData['pasw'] <> postData['cPasw']:
            errors['noMatch'] = "Your password doesnt match the confirm."
        if not errors:
            hashedPsw = bcrypt.hashpw(postData['pasw'].encode(), bcrypt.gensalt())
            b = User.objects.create(
                firstName = postData['fName'],
                lastName = postData['lName'],
                email = postData['email'],
                birthday = postData['birthday'],
                password = hashedPsw
            )
            b.save()
        return errors
    def validateLogin(self, postData):
        errors={}
        b = User.objects.filter(email = postData['email'])
        print b.values()[0]['password']
        if b:
            hashPasw = b.values()[0]['password']
            if not bcrypt.checkpw(postData['pasw'].encode(),b.values()[0]['password'].encode()):
                errors['pasw'] = "wrong Password"
        else:
            errors['email'] = "Wrong Email"
        return errors

class User(models.Model):
    firstName = models.CharField(max_length=20)
    lastName= models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    birthday = models.DateField()
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()