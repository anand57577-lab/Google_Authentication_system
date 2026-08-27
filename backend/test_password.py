from app.security.password import (
    hash_password,
    verify_password,
)


password = "Password@123"


hashed_password = hash_password(password)

print("Original password:")
print(password)

print("\nGenerated hash:")
print(hashed_password)

print("\nCorrect password:")
print(
    verify_password(
        password,
        hashed_password
    )
)

print("\nWrong password:")
print(
    verify_password(
        "WrongPassword@123",
        hashed_password
    )
)