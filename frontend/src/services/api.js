const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

console.log("API BASE URL:", API_BASE_URL);

if (!API_BASE_URL) {
  throw new Error("VITE_API_BASE_URL is not configured");
}

export async function registerUser(userData) {
  console.log("registerUser() called");
  console.log("Sending data:", userData);
  console.log("URL:", `${API_BASE_URL}/auth/register`);

  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });

  console.log("Response status:", response.status);

  const data = await response.json();

  console.log("Response data:", data);

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Registration failed"
    );
  }

  return data;
}

export async function loginUser(credentials) {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Login failed"
    );
  }

  return data;
}

export async function verifyEmail(token) {
  console.log("Verifying email...");
  console.log("Verification token:", token);

  const response = await fetch(`${API_BASE_URL}/auth/verify-email`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      token: token,
    }),
  });

  const data = await response.json();

  console.log("Verification response:", data);

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Email verification failed"
    );
  }

  return data;
}

export async function getCurrentUser() {
  const token = localStorage.getItem("access_token");

  if (!token) {
    throw new Error("Not authenticated");
  }

  const response = await fetch(`${API_BASE_URL}/auth/me`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Failed to get current user"
    );
  }

  return data;
}

export async function forgotPassword(email) {
  console.log("forgotPassword() called");
  console.log("Email:", email);

  const response = await fetch(
    `${API_BASE_URL}/auth/forgot-password`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email,
      }),
    }
  );

  const data = await response.json();

  console.log("Forgot password response:", data);

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Failed to send password reset email"
    );
  }

  return data;
}

export async function resetPassword(
  token,
  newPassword,
  confirmPassword
) {
  console.log("================================");
  console.log("resetPassword() called");
  console.log("Token:", token);
  console.log("New password:", newPassword);
  console.log("Confirm password:", confirmPassword);
  console.log("================================");

  const requestBody = {
    token: token,
    new_password: newPassword,
    confirm_password: confirmPassword,
  };

  console.log("RESET REQUEST BODY:", requestBody);

  const response = await fetch(
    `${API_BASE_URL}/auth/reset-password`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody),
    }
  );

  const data = await response.json();

  console.log("Reset password response:", data);

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Password reset failed"
    );
  }

  return data;
}

export async function resendVerification(email) {
  const response = await fetch(
    `${API_BASE_URL}/auth/resend-verification`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Unable to resend verification email"
    );
  }

  return data;
}