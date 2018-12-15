from django import forms
from .models import Comment, Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'photo',
        )

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'content',
                'placeholder': '댓글 달기...',
            }
        )
    )
    class Meta:
        model = Comment
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        print("__init__\n")
        self.fields['content'].error_messages = {'required': '댓글 내용을 입력해요~!!'}

    def clean_content(self):
        data = self.cleaned_data['content']
        print("asdf\n")
        print(self)
        print(data)
        errors = []
        if data is None or data == '':
            errors.append(forms.ValidationError('댓글 내용을 입력해주세요.'))
        if len(data) > 50:
            errors.append(forms.ValidationError('댓글 내용을 50자 이하로 입력해주세요....'))
        if errors:
            raise forms.ValidationError(errors)
        return data
