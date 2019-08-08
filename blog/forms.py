from django import forms
from .models import Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_title', 'post_contents']

        widgets = {
            'post_title': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width:100%', 'placeholder': '제목을 입력하세요.'}
            ),
            'post_contents': forms.CharField(widget=CKEditorUploadingWidget(attrs={'placeholder': '만날 장소, 수고비, 카톡아이디는 필수입니다!'})),
        }


class PostSearchForm(forms.Form):
    search_word = forms.CharField(label='검색 단어')



