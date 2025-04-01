- card.html
<div class="card my-3 p-0 col-12 col-md-6 col-xl-4"> # 두 줄 정렬 방식(레이)
<div class="card my-3 p-0 col-12 offset-md-3 col-md-6"> # 위로 한 줄 정렬

### 댓글 기능 구현
1. models.py class 설정
```shell
class Comment(models.Model):
    content = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```

2. makemigrations/ migrate 작업

3. forms.py class 설정
```shell
class CommentForm(ModelForm):
    class Meta():
        model = Comment
        fields = ('content',)
```


4. views.py 에서 만든 form 불러오고(from)
```shell
form = CommentForm()
    context = {
        'posts' : posts,
        'form': form
    }
```
- 뷰에서 데이터를 준비하고, 템플릿으로 전달하는 과정
form = CommentForm() → 댓글 폼 생성
context에 posts와 form을 저장
render(request, 'post_detail.html', context)로 템플릿에 데이터 전달
템플릿에서 {{ posts }}와 {{ form }}을 사용해서 출력

5. 
전달할 url 주소를 정하고
<form action="{% url 'posts:comment_create' post.id %}" method="POST">
url.py에 주소 설정
path('<int:post_id>/comments/create/', views.comment_create, name=comment_create),

post.id >> 각각의 게시물에 (몇 번 게시물?)


- 로그인 해야만 댓글 쓸 수 있도록 if문으로 구성
```shell
{% if user.is_authenticated %}
        <form action="{% url 'posts:comment_create' post.id %}" method="POST">
          {% csrf_token %}
          <div class="row">
            <div class="col-9">
              {% bootstrap_form form show_label=False wrapper_class='' %}

            </div>
            <div class="col-2">
              <input type="submit" class="btn btn-primary">

            </div>
          </div>
        </form>
        {% endif %}
```
# M:N 관계
  - 작성자 저장 필드
  ```shell
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
  ```
    - 이 글에 좋아요 누른 사람
    ```shell
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
    )
    ```

    중복 발생 >> Add or change a related_name argument to the definition for 'posts.Post.user' or 'posts.Post.like_users'
    > post_set(역참조) -> like_posts (MMF)

     <span>{{post.like_users.all}}명이 좋아합니다.</span> 
     좋아요 누른 사람의 리스트를 출력.
     >> 길이를 재면 됨 (|length)

    ### 팔로우 기능 
    