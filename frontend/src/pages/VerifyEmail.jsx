import { useSearchParams, useNavigate } from "react-router-dom";

function VerifyEmail() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const status = searchParams.get("status");

  // ==========================================
  // EMAIL VERIFIED SUCCESSFULLY
  // ==========================================
  if (status === "success") {
    return (
      <div className="auth-container">
        <div className="auth-card verify-card">

          <div className="verify-icon success-icon">
            ✓
          </div>

          <h2>Email Verified!</h2>

          <p className="auth-subtitle">
            Your email has been verified successfully.
          </p>

          <div className="verify-message success-message">
            <p>
              Your account is now active. You can log in
              and start using your account.
            </p>
          </div>

          <button
            type="button"
            className="primary-button"
            onClick={() => navigate("/login")}
          >
            Go to Login
          </button>

        </div>
      </div>
    );
  }

  // ==========================================
  // VERIFICATION LINK ALREADY USED
  // ==========================================
  if (status === "already-used") {
    return (
      <div className="auth-container">
        <div className="auth-card verify-card">

          <div className="verify-icon">
            ✓
          </div>

          <h2>Email Already Verified</h2>

          <p className="auth-subtitle">
            This verification link has already been used.
          </p>

          <div className="verify-message">
            <p>
              Your email address may already be verified.
              You can continue to login to your account.
            </p>
          </div>

          <button
            type="button"
            className="primary-button"
            onClick={() => navigate("/login")}
          >
            Go to Login
          </button>

        </div>
      </div>
    );
  }

  // ==========================================
  // VERIFICATION LINK EXPIRED
  // ==========================================
  if (status === "expired") {
    return (
      <div className="auth-container">
        <div className="auth-card verify-card">

          <div className="verify-icon error-icon">
            !
          </div>

          <h2>Verification Link Expired</h2>

          <p className="auth-subtitle">
            This verification link is no longer valid.
          </p>

          <div className="verify-message error-message">
            <p>
              Please request a new verification email and
              try again.
            </p>
          </div>

          <button
            type="button"
            className="primary-button"
            onClick={() => navigate("/login")}
          >
            Go to Login
          </button>

        </div>
      </div>
    );
  }

  // ==========================================
  // INVALID VERIFICATION LINK
  // ==========================================
  if (status === "invalid") {
    return (
      <div className="auth-container">
        <div className="auth-card verify-card">

          <div className="verify-icon error-icon">
            !
          </div>

          <h2>Invalid Verification Link</h2>

          <p className="auth-subtitle">
            We couldn't verify your email address.
          </p>

          <div className="verify-message error-message">
            <p>
              The verification link may be invalid or no
              longer available.
            </p>
          </div>

          <button
            type="button"
            className="primary-button"
            onClick={() => navigate("/login")}
          >
            Go to Login
          </button>

        </div>
      </div>
    );
  }

  // ==========================================
  // DEFAULT: CHECK YOUR EMAIL
  // ==========================================
  return (
    <div className="auth-container">
      <div className="auth-card verify-card">

        <div className="verify-icon">
          ✉
        </div>

        <h2>Check Your Email</h2>

        <p className="auth-subtitle">
          We've sent a verification link to your email
          address.
        </p>

        <div className="verify-message">
          <p>
            Please check your inbox and click the
            verification link to activate your account.
          </p>
        </div>

        <p className="verify-help">
          Didn't receive the email?
        </p>

        <button
          type="button"
          className="secondary-button"
          onClick={() => navigate("/login")}
        >
          Go to Login
        </button>

        <button
          type="button"
          className="text-button verify-login-link"
          onClick={() => navigate("/login")}
        >
          Back to Login
        </button>

      </div>
    </div>
  );
}

export default VerifyEmail;