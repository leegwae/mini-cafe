## 실행
`docker-compose up` 실행 후 `django | Starting development server at http://0.0.0.0:8000/` 뜰때까지 기다리기.

회원가입 및 로그인 후 http://localhost:8000/api/ 또는 http://localhost:8000/swagger/ 에서 주문접수.

## 프로토타입 

<img src="client/img/index.png" width="480px">
<img src="client/img/bot.png" width="480px">

## 요구사항

✅️ 완료한 것

* 장고 기본 User 를 활용한 로그인/회원가입 
  * 바리스타 / 일반멤버 선택 (AbstratUser 상속 후 재정의)
* index 에서 메뉴 재고 총합, 받은 주문 개수 표시하기 
* 일정 시간마다 전체 유저 포인트 추가 / 메뉴 재고 추가
  * `api/tasks.py` 에 celery 태스크 정의하고 `config/celery.py` 에서 스케줄 설정
    
    `select_for_update()` 로 테이블 lock 걸고 `bulk_update()` 로 최적화 
    
* 메뉴주문 api 에 트랜잭션, 메세지 큐 적용 
  * 재고 차감과 포인트 차감을 트랜잭션으로 묶어서 ACID 하게 주문 접수 `api/views.py`
  
    주문 내용 db 에 저장 후 메세지 큐에 보냄 `api/tasks.py`

* 테스트케이스 작성
  * 성공 테스트케이스 작성 
  * 트랜잭션 충돌 테스트 작성하기 ➕ 
  * celery 스케줄러 테스트 방법? ➕

➕ 추가할 것️(TODO)

* 바리스타 전용 재고 주문 페이지 생성
  * 주기적으로 재고 업데이트 되는 시간 외에 추가로 재고 주문할 수 있게 하기
  * permissions 적용해서 일반멤버/바리스타 뷰 접근 제어하기

* 현재 주문량 실시간 확인
  * 일반멤버: 지금 주문하면 몇분후에 받을 수 있는지. 내 대기번호가 몇번인지 확인. 
  
    redis 를 파이썬에서 확인하는법(?) 알아볼것.
  * 바리스타: 현재 주문량에 비해 재고가 얼마나 남았는지 확인하기 
    
    예: 재고10개, 주문량 12개, 재고 배달까지 남은시간 30분이면, N분 후에 재고가 모자랄 것을 미리 예측

* 웹소켓 활용해서 실시간 통신하기 (django channels)
  * index 페이지의 메뉴 숫자. 재고가 업데이트 될때마다 변경하기 
  * 주문 완료시 bot 에 표시하기


## 참고자료
### reference
* https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html
* https://hakibenita.medium.com/how-to-manage-concurrency-in-django-models-b240fed4ee2
* https://medium.com/@alexandre.laplante/djangos-select-for-update-with-examples-and-tests-caff09414766
* https://techblog.woowahan.com/2547/
* https://medium.com/@erayerdin/how-to-test-celery-in-django-927438757daf