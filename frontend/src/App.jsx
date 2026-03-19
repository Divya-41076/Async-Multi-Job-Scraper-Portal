import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  useLocation,
} from "react-router-dom";
import Jobs from "./pages/Jobs";
import Admin from "./pages/Admin";

function Navbar() {
  const location = useLocation();

  return (
    <nav className="bg-gray-900 border-b border-gray-800 px-6 py-4 flex items-center justify-between">
      <span className="text-white font-bold text-lg tracking-tight">
        Job<span className="text-emerald-500">Pulse</span>
      </span>
      <div className="flex gap-6">
        <Link
          to="/"
          className={`text-sm font-medium transition-colors ${
            location.pathname === "/"
              ? "text-emerald-500"
              : "text-gray-400 hover:text-white"
          }`}
        >
          Jobs
        </Link>

        <Link
          to="/admin"
          className={`text-sm font-medium transition-colors ${
            location.pathname === "/admin"
              ? "text-emerald-500"
              : "text-gray-400 hover:text-white"
          }`}
        >
          Admin
        </Link>
      </div>
    </nav>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-950">
        <Navbar />
        <Routes>
          <Route path="/" element={<Jobs />} />
          <Route path="/admin" element={<Admin />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
