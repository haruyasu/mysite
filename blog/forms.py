from django import forms
from blog.models import Post, Comment
from django.core import validators
from django.core.mail import send_mail
from django.conf import settings

class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        subject = self.cleaned_data['name']
        message = self.cleaned_data['message'] + self.cleaned_data['email']
        from_email = settings.EMAIL_HOST_USER
        to = [settings.EMAIL_HOST_USER]

        send_mail(subject, message, from_email, to)

class FormName(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    botcatcher = forms.CharField(required=False, widget=forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

    def clean(self):
        all_clean_data = super().clean()


class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('author', 'title', 'text', 'image')
        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }

class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('author', 'text')
        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }
