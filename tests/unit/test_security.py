from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_password():
    password = "mysecretpassword"
    hashed = hash_password(password)

    # Хэш не равен оригиналу
    assert hashed != password
    # Хэш всегда разный (соль)
    assert hashed != hash_password(password)


def test_verify_password_correct():
    password = "mysecretpassword"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True


def test_verify_password_wrong():
    hashed = hash_password("correct_password")
    assert verify_password("wrong_password", hashed) is False


def test_create_and_decode_token():
    subject = "test-company-id"
    token = create_access_token(subject)

    # Токен создался
    assert token is not None
    assert len(token) > 0

    # Декодируется правильно
    decoded = decode_access_token(token)
    assert decoded == subject


def test_decode_invalid_token():
    result = decode_access_token("invalid.token.here")
    assert result is None
