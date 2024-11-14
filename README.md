# FastAPI_Practice

## blogAPI

간단한 형식의 게시글을 작성 할 수 있는 API

- GET: 127.0.0.1:8000/post/
게시글 목록

<br>

- POST: 127.0.0.1:8000/post/create
게시글 생성. 아래의 형식으로 응답을 보낼 수 있습니다.

```json
{
  "title": "fastAPI 테스트",
  "description": "간단한 blog post 기능 구현하기",
  "author": {
    "name": "user",
    "email": "user@example.com"
  }
}
```

<br>

- GET: 127.0.0.1:8000/post/{post_id}
게시글의 id로 자세한 정보를 확인할 수 있습니다.

<br>

- PUT 127.0.0.1:8000/post/{post_id}
특정 게시글의 정보를 변경할 수 있습니다.


## calculatorAPI

매개변수를 이용해 URL로 계산기를 구현한 API
