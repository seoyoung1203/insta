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
    
    likeRequest >> 밑에서 호출 -> 두 가지 필요(Btn, postId 필요)

    딕셔너리를 json으로 바꾼 다음 이용자에게 전송

    --------

    # 2025/04/04

    - sudo apt-get update
    pip 기준으로 최신화 할게요

    - sudo apt-get install -y nginx
    sudo apt-get install nginx인데 나오는거 다 예스 할게욤
    --------

# deploy

0. settings.py
ALLOWED_HOSTS
EC2 서버주소를 등록
편하게 배포하기 위하여 * 로 등록 후 추후 수정가능
### settings.py
ALLOWED_HOSTS = [
    '.compute.amazonaws.com',
    '*',
]
​
1. 의존성 저장
freeze
pip freeze > requirements.txt
​
2. git push
원격저장소에 업로드 (add, commit, push)

AWS 가입 (https://aws.amazon.com/ko/) (선택)
AWS 계정 생성
기본정보입력
카드정보입력
휴대폰인증
완료후 로그인
EC2

0. 인스턴스 생성
Ubuntu Server 24.04 LTS
키 페어 > 새 키페어 생성
.pem(linux)
.ppk(window)

1. 인바운드 설정
인스턴스 ID > 보안 > 보안그룹 ID > 인바운드 규칙 편집

SSH
pem키 권한 수정
window : 속성 > 권한설정

~로 이동 => cd ~

클론한 폴더로 이동
cd {프로젝트이름}/
​
venv
python -m venv venv
source venv/bin/activate
​
install package
pip install -r requirements.txt
​
migration
python manage.py migrate
​
createsuperuser
python manage.py createsuperuser
​
- nginx
0. 설치
sudo apt-get update
sudo apt-get install -y nginx
​

파일 수정
sudo vi /etc/nginx/sites-enabled/default
​
아래의 표시된 부분 수정
i 버튼으로 수정모드로 전환
아래의 부분으로 방향키를 이용하여 이동
수정
esc 로 수정모드 빠져나오기
:wq 명령어로 저장 후 종료

​
등록
# daemon reload
sudo systemctl daemon-reload

# uswgi daemon enable and restart
sudo systemctl enable uwsgi
sudo systemctl restart uwsgi.service

# check daemon
sudo systemctl | grep nginx
sudo systemctl | grep uwsgi

# restart
sudo systemctl restart nginx
sudo systemctl restart uwsgi