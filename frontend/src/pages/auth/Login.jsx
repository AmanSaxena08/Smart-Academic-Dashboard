import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import API from "../../api/axios";

// One-click demo accounts so reviewers can explore without typing credentials.
const DEMO_ACCOUNTS = [
  {
    role: "Student",
    username: "s6a01",
    password: "Student@1234",
    blurb: "attendance, marks, timetable",
    styles: "border-indigo-200 bg-indigo-50 text-indigo-700 hover:bg-indigo-100",
  },
  {
    role: "Faculty",
    username: "prof_sharma",
    password: "Faculty@1234",
    blurb: "mark attendance, Excel/PDF reports",
    styles: "border-emerald-200 bg-emerald-50 text-emerald-700 hover:bg-emerald-100",
  },
  {
    role: "HOD",
    username: "hod_cs",
    password: "HOD@1234",
    blurb: "department stats, notice board",
    styles: "border-amber-200 bg-amber-50 text-amber-700 hover:bg-amber-100",
  },
];

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const signIn = async (credentials) => {
    setError("");
    setLoading(true);
    try {
      const res = await API.post("/users/login/", credentials);
      login(res.data.user, res.data.access, res.data.refresh);
      if (res.data.user.role === "student") navigate("/student/home");
      else if (res.data.user.role === "faculty") {
        if (res.data.user.is_hod) navigate("/hod/home");
        else navigate("/faculty/home");
      }
    } catch (err) {
      setError(err.response?.data?.error || "Invalid credentials");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    signIn(formData);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
  <div className="bg-white rounded-2xl shadow-xl w-full max-w-md p-6 lg:p-8">

        {/* Header */}
        <div className="text-center mb-8">
          <div className="bg-indigo-600 text-white w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4 text-2xl font-bold text-white">
            SA
          </div>
          <h1 className="text-2xl font-bold text-black text-gray-800">Smart Academic</h1>
          <p className="text-gray-500 text-sm mt-1">Sign in to your account</p>
        </div>

        {/* Error */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg mb-6 text-sm">
            {error}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="Enter your username"
              required
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter your password"
              required
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 rounded-lg transition duration-200 text-sm disabled:opacity-50"
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>

        {/* Demo accounts — credentials shown, tap to sign in */}
        <div className="mt-6">
          <div className="flex items-center gap-3 mb-3">
            <div className="h-px bg-gray-200 flex-1" />
            <span className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
              Demo Accounts
            </span>
            <div className="h-px bg-gray-200 flex-1" />
          </div>

          <p className="text-xs text-gray-500 text-center mb-3">
            Tap any card to sign in instantly, or type the credentials above.
          </p>

          <div className="space-y-2">
            {DEMO_ACCOUNTS.map((acct) => (
              <button
                key={acct.role}
                type="button"
                disabled={loading}
                onClick={() =>
                  signIn({ username: acct.username, password: acct.password })
                }
                className={`w-full px-4 py-3 border rounded-lg text-left transition duration-200 disabled:opacity-50 ${acct.styles}`}
              >
                <div className="flex items-center justify-between gap-2 mb-1.5">
                  <span className="text-sm font-bold">{acct.role}</span>
                  <span className="text-[10px] font-semibold opacity-60 whitespace-nowrap">
                    TAP TO SIGN IN &rarr;
                  </span>
                </div>
                <div className="font-mono text-xs opacity-90 flex flex-wrap gap-x-2">
                  <span>{acct.username}</span>
                  <span className="opacity-50">/</span>
                  <span>{acct.password}</span>
                </div>
                <div className="text-[11px] opacity-60 mt-1">{acct.blurb}</div>
              </button>
            ))}
          </div>

          <p className="text-[11px] text-gray-400 text-center mt-3">
            Shared demo data &mdash; no sign-up required.
          </p>
        </div>

        {/* Register Link */}
        <p className="text-center text-sm text-gray-500 mt-6">
          New student?{" "}
          <Link to="/register" className="text-indigo-600 font-semibold hover:underline">
            Register here
          </Link>
        </p>

        {/* Role Info
        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <p className="text-xs text-gray-500 text-center font-medium mb-2">Login redirects by role</p>
          <div className="flex justify-center gap-4">
            <span className="text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded-full">Student → Student Dashboard</span>
            <span className="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full">Faculty → Faculty Dashboard</span>
          </div>
        </div> */}

      </div>
    </div>
  );
}