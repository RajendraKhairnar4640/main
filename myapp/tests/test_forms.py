from django.test import TestCase
from django.test import Client
from myapp.forms import RegisterForm,NewCommentForm,NewPostForm
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.conf import settings

class Setup_Class(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="raj@gmail.com",username="rk",password="Raj@4640")
    
    def test_registration_form_valid(self):

        form = RegisterForm(data={
            'email':"raj@gmail.com",
            'username':"raj123",
            'password1':"Raj@4640",
            'password2':"Raj@4640"
        })
        #print("form error",form.errors)
        self.assertTrue(form.is_valid())

    def test_registration_form_invalid(self):
        form = RegisterForm(data={})
        self.assertFalse(form.is_valid())

    def test_post_form_valid(self):
        BASE_DIR = settings.BASE_DIR
        self.pic_file = open(
            os.path.join(BASE_DIR, 'myapp/static/myapp/images/ganesh.jpg'), "rb"
        )
        # breakpoint()        
        data={
            'description':'instagram',
            'tags':'social',
        }
        
        files_data ={
            'pic':SimpleUploadedFile(
                self.pic_file.name,
                self.pic_file.read()
            )
        }
        form = NewPostForm(data=data,files=files_data)
        self.assertTrue(form.is_valid())

    def test_post_form_invalid(self):
        form = NewPostForm(data={})
        self.assertFalse(form.is_valid())

    def test_comment_form_valid(self):
        form = NewCommentForm(data={
            'comment':'hello django',
        })
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid(self):
        form = NewCommentForm(data={'comment':''})
        self.assertFalse(form.is_valid())