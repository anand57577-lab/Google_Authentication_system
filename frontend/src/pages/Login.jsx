import { useState } from "react";
import { Mail, Lock } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { loginUser, resendVerification } from "../services/api";

function Login() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setMessage("");
    setError("");

    try {
      setLoading(true);

      const data = await loginUser(formData);

      localStorage.setItem(
        "access_token",
        data.access_token
      );

      localStorage.setItem(
        "refresh_token",
        data.refresh_token
      );

      setMessage("Login successful!");

      navigate("/dashboard");

    } catch (err) {
      console.error("Login error:", err);

      setError(
        err.message || "Login failed"
      );

    } finally {
      setLoading(false);
    }
  };

  const handleGoogleLogin = () => {
    window.location.href =
      `${import.meta.env.VITE_API_BASE_URL}/auth/google/login`;
  };

  const handleResendVerification = async () => {
    setMessage("");
    setError("");

    if (!formData.email) {
      setError("Please enter your email first.");
      return;
    }

    try {
      setLoading(true);

      const data = await resendVerification({
        email: formData.email,
      });

      setMessage(
        data.message ||
        "Verification email sent successfully."
      );

    } catch (err) {
      console.error(
        "Resend verification error:",
        err
      );

      setError(
        err.message ||
        "Unable to resend verification email."
      );

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">

      <div className="auth-card">

        {/* Header */}
        <div className="auth-header">

          <h2>Welcome Back</h2>

          <p className="auth-subtitle">
            Login to your account
          </p>

        </div>


        {/* Messages */}

        {message && (
          <div className="success-message">
            {message}
          </div>
        )}

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}


        {/* Login Form */}

        <form
          onSubmit={handleSubmit}
          className="auth-form"
        >

          {/* Email */}

          <div className="form-group">

            <label htmlFor="email">
              Email
            </label>

            <div className="input-wrapper">

              

              <input
                id="email"
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="Enter your email"
                required
              />

            </div>

          </div>


          {/* Password */}

          <div className="form-group">

            <label htmlFor="password">
              Password
            </label>

            <div className="input-wrapper">

              

              <input
                id="password"
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Enter your password"
                required
              />

            </div>

          </div>


          {/* Recovery Links */}

          <div className="login-options">

            <button
              type="button"
              className="text-button"
              onClick={() =>
                navigate("/forgot-password")
              }
            >
              Forgot Password?
            </button>

            <button
              type="button"
              className="text-button"
              onClick={handleResendVerification}
            >
              Resend Verification
            </button>

          </div>


          {/* Login */}

          <button
            type="submit"
            className="primary-button"
            disabled={loading}
          >
            {loading ? "Logging in..." : "Login"}
          </button>


          {/* Divider */}

          <div className="divider">

            <span></span>

            <p>OR</p>

            <span></span>

          </div>


          {/* Google */}

          <button
            type="button"
            className="google-button"
            onClick={handleGoogleLogin}
          >

            <span className="google-logo">
              G
            </span>

            <span>
              Continue with Google
            </span>

          </button>


          {/* Register */}

          <p className="auth-switch">

            Don't have an account?{" "}

            <button
              type="button"
              className="link-button"
              onClick={() =>
                navigate("/register")
              }
            >
              Register
            </button>

          </p>

        </form>

      </div>

    </div>
  );
}

export default Login;