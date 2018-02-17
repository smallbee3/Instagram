from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, Comment
from .forms import CommentForm


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'post/post_list.html', context)


def comment_create(request, post_pk):
    # 요청 메서드가 POST방식 일 때만 처리
    if request.method == 'POST':
        # Post인스턴스를 가져오거나 404 Response를 돌려줌
        post = get_object_or_404(Post, pk=post_pk)

    # 04. Post에 Comment추가하기
    #   -> 뷰에서 처리
    #     # request.POST에서 'content'키의 값을 가져옴
    #     content = request.POST.get('content')
    #
    #     # 'content'키가 없었거나 내용이 입력되지 않았을 경우
    #     if not content:
    #         # 400(BadRequest)로 응답을 전송
    #         return HttpResponse('댓글 내용을 입력하세요', status=400)
    #
    #     # 내용이 전달 된 경우, Comment객체를 생성 및 DB에 저장
    #     Comment.objects.create(
    #         post=post,
    #         # 작성자는 현재 요청의 사용자로 지정
    #         author=request.user,
    #         content=content
    #     )
    #     # 정상적으로 Comment가 생성된 후
    #     # 'post'네임스페이스를 가진 url의 'post_list'이름에 해당하는 뷰로 이동
    #     return redirect('post:post_list')


    # 05. Comment생성에 Form클래스 사용
    #   -> form.py의 CommentForm에서 처리
    #     # request.POST데이터를 이용한 Bounded Form생성
    #     comment_form = CommentForm(request.POST)
    #     # 올바른 데이터가 Form인스턴스에 바인딩 되어있는지 유효성 검사
    #     if comment_form.is_valid():
    #         # 유효성 검사에 통과하면 Comment객체 생성 및 DB저장
    #         Comment.objects.create(
    #             post=post,
    #             # 작성자는 현재 요청의 사용자로 지정
    #             author=request.user,
    #             content=comment_form.cleaned_data['content']
    #         )
    #         # 정상적으로 Comment가 생성된 후
    #         # 'post'네임스페이스를 가진 url의 'post_list'이름에 해당하는 뷰로 이동
    #         return redirect('post:post_list')


    # 06. 메시지 프레임워크를 사용해서 에러메시지 출력
    #   -> 다음 요청시 전달할 메시지를 messages모듈을 사용해 추가
    #
        # request.POST데이터를 이용한 Bounded Form생성
        comment_form = CommentForm(request.POST)
        # 올바른 데이터가 Form인스턴스에 바인딩 되어있는지 유효성 검사
        if comment_form.is_valid():
            # 유효성 검사에 통과하면 ModelForm의 save()호출로 인스턴스 생성
            # DB에 저장하지 않고 인스턴스만 생성하기 위해 commit=False옵션 지정
            comment = comment_form.save(commit=False)
            # CommentForm에 지정되지 않았으나 필수요소인 author와 post속성을 지정
            comment.post = post
            comment.author = request.user
            # DB에 저장
            comment.save()

            # 성공 메시지를 다음 request의 결과로 전달하도록 지정
            messages.success(request, '댓글이 등록되었습니다')
        else:
            # 유효성 검사에 실패한 경우
            # 에러 목록을 순회하며 에러메시지를 작성, messages의 error레벨로 추가
            error_msg = '댓글 등록에 실패했습니다\n{}'.format(
                '\n'.join(
                    [f'- {error}'
                     for key, value in comment_form.errors.items()
                     for error in value]))
            messages.error(request, error_msg)

        # comment_form이 valid하건 하지않건
        # 'post'네임스페이스를 가진 url의 'post_list'이름에 해당하는 뷰로 이동
        return redirect('post:post_list')
