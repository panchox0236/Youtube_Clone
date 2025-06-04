from django import forms
from .models import User, Channel

class UserRegistrationForm(forms.ModelForm):
    user_type = forms.ChoiceField(
    choices=User.USER_TYPE_CHOICES, 
    label="User Type",
    initial=User.STANDARD
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type']
        widgets = {
            'password': forms.PasswordInput(),
        }
class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['channel_name', 'description', 'channel_pic']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }