import { useState } from "react";
import {
  useNavigate,
  useSearchParams,
} from "react-router-dom";
import { resetPassword } from "../services/api";

function ResetPassword() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const token = searchParams.get("token");

  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setMessage("");
    setError("");

    if (!token) {
      setError(
        "Invalid or missing password reset token."
      );
      return;
    }

    if (newPassword !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    try {
      setLoading(true);

      console.log("Resetting password...");

      const data = await resetPassword(
        token,
        newPassword,
        confirmPassword
      );

      console.log(
        "Password reset successful:",
        data
      );

      // Show success message
      setMessage(
        data.message ||
          "Password changed successfully."
      );

      // Clear password fields
      setNewPassword("");
      setConfirmPassword("");

      // Redirect to login after 2 seconds
      setTimeout(() => {
        navigate("/login", {
          replace: true,
        });
      }, 2000);

    } catch (err) {
      console.error(
        "Reset password error:",
        err
      );

      setError(
        err.message ||
          "Password reset failed."
      );

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">

        <h2>Reset Password</h2>

        <p className="auth-subtitle">
          Enter your new password below.
        </p>


        {/* ================================
            SUCCESS MESSAGE
        ================================= */}

        {message && (
          <div className="success-message">
            ✓ {message}

            <p className="redirect-message">
              Redirecting you to login...
            </p>
          </div>
        )}


        {/* ================================
            ERROR MESSAGE
        ================================= */}

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}


        {/* ================================
            INVALID TOKEN
        ================================= */}

        {!token ? (
          <div className="reset-invalid">

            <p>
              This password reset link is
              invalid or incomplete.
            </p>

            <button
              type="button"
              className="primary-button"
              onClick={() =>
                navigate("/forgot-password")
              }
            >
              Request New Link
            </button>

          </div>
        ) : (

          /* ================================
             RESET PASSWORD FORM
          ================================= */

          !message && (
            <form onSubmit={handleSubmit}>

              <label>
                New Password
              </label>

              <input
                type="password"
                value={newPassword}
                onChange={(e) =>
                  setNewPassword(
                    e.target.value
                  )
                }
                placeholder="Enter new password"
                required
                disabled={loading}
              />


              <label>
                Confirm New Password
              </label>

              <input
                type="password"
                value={confirmPassword}
                onChange={(e) =>
                  setConfirmPassword(
                    e.target.value
                  )
                }
                placeholder="Confirm new password"
                required
                disabled={loading}
              />


              <button
                type="submit"
                className="primary-button"
                disabled={loading}
              >
                {loading
                  ? "Resetting..."
                  : "Reset Password"}
              </button>

            </form>
          )
        )}

      </div>
    </div>
  );
}

export default ResetPassword;