import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

function GoogleCallback() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  useEffect(() => {
    const accessToken = searchParams.get("access_token");
    const refreshToken = searchParams.get("refresh_token");

    console.log("Google callback received");

    if (!accessToken || !refreshToken) {
      console.error("Google authentication tokens are missing");
      navigate("/login");
      return;
    }

    // Store authentication tokens
    localStorage.setItem("access_token", accessToken);
    localStorage.setItem("refresh_token", refreshToken);

    console.log("Google authentication successful");

    // Go to dashboard
    navigate("/dashboard", { replace: true });
  }, [navigate, searchParams]);

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Signing you in...</h2>
        <p className="auth-subtitle">
          Please wait while we complete Google authentication.
        </p>
      </div>
    </div>
  );
}

export default GoogleCallback;