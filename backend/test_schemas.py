from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
)


# -------------------------
# Valid registration
# -------------------------

valid_user = RegisterRequest(
    full_name="Anand",
    email="anand@example.com",
    password="Password@123",
    confirm_password="Password@123"
)

print("Valid registration:")
print(valid_user)


# -------------------------
# Valid login
# -------------------------

valid_login = LoginRequest(
    email="anand@example.com",
    password="Password@123"
)

print("\nValid login:")
print(valid_login)

print("\nTesting invalid password...")

try:

    RegisterRequest(
        full_name="Anand",
        email="anand@example.com",
        password="password",
        confirm_password="password"
    )

except Exception as e:

    print(e)

print("\nTesting mismatched passwords...")

try:

    RegisterRequest(
        full_name="Anand",
        email="anand@example.com",
        password="Password@123",
        confirm_password="Password@456"
    )

except Exception as e:

    print(e)