import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { resendVerification } from "../services/api";

function ResendVerification() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setMessage("");
    setError("");

    try {
      setLoading(true);

      const data = await resendVerification(email);

      setMessage(
        data.message ||
          "A new verification email has been sent."
      );
    } catch (err) {
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
        <h2>Verify Your Email</h2>

        <p className="auth-subtitle">
          Didn't receive the verification email?
          Enter your email below.
        </p>

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

        <form onSubmit={handleSubmit}>
          <label>Email</label>

          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
            required
          />

          <button type="submit" disabled={loading}>
            {loading
              ? "Sending..."
              : "Resend Verification Email"}
          </button>
        </form>

        <button
          type="button"
          onClick={() => navigate("/login")}
        >
          Back to Login
        </button>
      </div>
    </div>
  );
}

export default ResendVerification;