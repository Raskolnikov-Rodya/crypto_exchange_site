from fastapi import HTTPException

from App.core.security import get_password_hash, validate_password_strength, verify_password


def test_password_hash_and_verify_over_72_chars() -> None:
    password = "A" * 80 + "1"
    hashed = get_password_hash(password)
    assert hashed.startswith("$pbkdf2-sha256$")
    assert verify_password(password, hashed)


def test_password_strength_rejects_too_long() -> None:
    too_long = "A" * 129 + "1"
    try:
        validate_password_strength(too_long)
        assert False, "Expected HTTPException"
    except HTTPException as exc:
        assert exc.status_code == 400
        assert "at most 128" in str(exc.detail)


def test_verify_password_handles_invalid_hash_gracefully() -> None:
    assert verify_password("SecurePass1", "not-a-real-hash") is False
