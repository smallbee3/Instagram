# from django.forms import forms
# 위에거 아님 조심.

from django import forms

# 05. Comment생성에 Form클래스 사용
from .models import Comment


# 05. Comment생성에 Form클래스 사용
# class CommentForm(forms.Form):
#     # content = forms.CharField(
#     #     widget=forms.TextInput(
#     #         attrs={
#     #             'class': 'content',
#     #             'placeholder': '댓글 달기...',
#     #         }
#     #     )
#     # )
#
#     attrs = {'class': 'content', 'placeholder': '댓글 달기...'}
#
#     # 왜 안되는지 의문
#     # widget = forms.TextInput(attrs)
#     # content = forms.CharField(widget)
#     content = forms.CharField(widget = forms.TextInput(attrs))


# 07. ModelForm을 사용하도록 CommentForm 리팩토링
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'content',
        )
        widgets = {
            'content': forms.TextInput(
                attrs={
                    'class': 'content',
                    'placeholder': '댓글 달기...',
                }
            )
        }


# 06. 메시지 프레임워크를 사용해서 에러메시지 출력

    def clean_content(self):
        data = self.cleaned_data['content']
        errors = []
        if data == '':
            errors.append(forms.ValidationError('댓글 내용을 입력해주세요'))
        elif len(data) > 50:
            errors.append(forms.ValidationError('댓글 내용은 50자 이하로 입력해주세요'))
        if errors:
            raise forms.ValidationError(errors)
        return data