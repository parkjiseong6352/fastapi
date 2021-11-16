from starlette import status
from enum import Enum


class Http2XX(Enum):
    SUCCESS = ("S000", "성공", status.HTTP_200_OK)
    CREATED = ("S001", "생성 완료", status.HTTP_201_CREATED)


class Http4XX(Enum):
    BAE_REQUEST = ("E000", "잘못된 요청", status.HTTP_400_BAD_REQUEST) 
    UNAUTHORIZED = ("E001", "인증 정보 없음", status.HTTP_401_UNAUTHORIZED)
    JWT_DecodeError = ("E002", "Decode 에러", status.HTTP_401_UNAUTHORIZED)
    JWT_ExpiredSignature = ("E003", "토큰 만료", status.HTTP_401_UNAUTHORIZED)
    JWT_InvalidTokenError = (
        "E004", "유효하지 않은 토큰", status.HTTP_401_UNAUTHORIZED
    )
    REGISTERED_EMAIL = (
        "E005", "이미 등록된 계정입니다.", status.HTTP_400_BAD_REQUEST
    )
    INCORRECT_PASSWORD = (
        "E006", "비밀번호가 일치하지 않습니다.", status.HTTP_400_BAD_REQUEST
    )
    INVALID_EMAIL = (
        "E007", "가입하지 않은 계정입니다.", status.HTTP_400_BAD_REQUEST
    )


class Http5XX(Enum):
    SERVER_ERROR = (
        "F000", "알 수 없는 에러", status.HTTP_500_INTERNAL_SERVER_ERROR
    )
