import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { registerUser } from "../services/api";

function Register() {
  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    password: "",
    confirm_password: "",
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

    console.log("================================");
    console.log("REGISTER FORM SUBMITTED");
    console.log("================================");

    setMessage("");
    setError("");

    if (formData.password !== formData.confirm_password) {
      console.log("Passwords do not match");
      setError("Passwords do not match");
      return;
    }

    try {
      setLoading(true);

      console.log("Calling registerUser...");

      const data = await registerUser(formData);

      console.log("Registration successful:", data);
      navigate("/verify-email", {
        state: {
          email: formData.email,
          message:
            data.message ||
            "Your account has been created. Please verify your email to continue.",
        },
      });

    } catch (err) {
      console.error("Registration error:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Create Account</h2>
        <p className="auth-subtitle">Register for your account</p>

        <form onSubmit={handleSubmit}>
          <label>Full Name</label>
          <input
            type="text"
            name="full_name"
            value={formData.full_name}
            onChange={handleChange}
            placeholder="Enter your full name"
            required
          />

          <label>Email</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="Enter your email"
            required
          />

          <label>Password</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Enter your password"
            required
          />

          <label>Confirm Password</label>
          <input
            type="password"
            name="confirm_password"
            value={formData.confirm_password}
            onChange={handleChange}
            placeholder="Confirm your password"
            required
          />

          <button type="submit">Create Account</button>

          <p className="auth-switch">
            Already have an account?{" "}
            <button
              type="button"
              onClick={() => navigate("/login")}
              className="link-button"
            >
              Login
            </button>
          </p>
        </form>
      </div>
    </div>
  );
}

export default Register;