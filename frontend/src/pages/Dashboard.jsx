import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getCurrentUser } from "../services/api";

function Dashboard() {
  const navigate = useNavigate();

  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadUser = async () => {
      try {
        const data = await getCurrentUser();

        console.log("Current user:", data);

        setUser(data);
      } catch (err) {
        console.error("Failed to load user:", err);

        localStorage.removeItem("access_token");
        setError(err.message);

        navigate("/login", { replace: true });
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/login", { replace: true });
  };

  if (loading) {
    return (
      <div className="auth-container">
        <div className="auth-card">
          <h2>Loading...</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Welcome 👋</h2>

        {user && (
          <>
            <p>
              <strong>Name:</strong> {user.full_name}
            </p>

            <p>
              <strong>Email:</strong> {user.email}
            </p>
          </>
        )}

        {error && <p>{error}</p>}

        <button onClick={handleLogout}>
          Logout
        </button>
      </div>
    </div>
  );
}

export default Dashboard;