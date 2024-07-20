---
name: Test
about: 테스트 작성 템플릿
title: 'TEST: '
labels: test
assignees: ZeyaKim

---

# TEST: #43-StandardSignUpAPITestCase

## 정보
| 항목 | 내용 |
|------|------|
| REQ | #43 |
| 타입 | Integration |
| TC명 | StandardSignUpAPITestCase |

## test_successful_signup
### test_successful_signup
### Scenario
#### Given
- 테스트용 데이터베이스가 초기화되어 있다.
- API 엔드포인트가 설정되어 있다.
#### When
- `/api/signup`에 POST 요청을 보낸다.
- 요청 본문: `{"email": "newuser@example.com", "password": "SecurePass123!"}`
#### Then
- 응답 상태 코드가 201이다.
- 응답 본문에 성공 메시지와 사용자 ID가 포함되어 있다.
- 데이터베이스에 새 사용자 정보가 저장되어 있다.
- 저장된 비밀번호가 해시화되어 있다.

## test_duplicate_email_signup
### test_duplicate_email_signup
### Scenario
#### Given
- 테스트용 데이터베이스에 기존 사용자 정보가 입력되어 있다.
- API 엔드포인트가 설정되어 있다.
#### When
- `/api/signup`에 POST 요청을 보낸다.
- 요청 본문: `{"email": "existinguser@example.com", "password": "AnotherPass456!"}`
#### Then
- 응답 상태 코드가 400이다.
- 응답 본문에 중복 이메일 오류 메시지가 포함되어 있다.
- 데이터베이스에 새 사용자 정보가 추가되지 않았다.

## test_invalid_email_format
### test_invalid_email_format
### Scenario
#### Given
- API 엔드포인트가 설정되어 있다.
#### When
- `/api/signup`에 POST 요청을 보낸다.
- 요청 본문: `{"email": "invalidemail", "password": "ValidPass789!"}`
#### Then
- 응답 상태 코드가 400이다.
- 응답 본문에 이메일 형식 오류 메시지가 포함되어 있다.

## test_password_policy_violation
### test_password_policy_violation
### Scenario
#### Given
- API 엔드포인트가 설정되어 있다.
#### When
- `/api/signup`에 POST 요청을 보낸다.
- 요청 본문: `{"email": "newuser2@example.com", "password": "weak"}`
#### Then
- 응답 상태 코드가 400이다.
- 응답 본문에 비밀번호 정책 위반 오류 메시지가 포함되어 있다.
