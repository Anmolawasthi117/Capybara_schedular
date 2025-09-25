import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import AdminPanel from "./pages/AdminPanel";
import OverviewPage from "./pages/OverviewPage";

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* <Navbar /> */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/admin" element={<AdminPanel />} />
        <Route path="/overview" element={<OverviewPage />} />
      </Routes>
    </div>
  );
}

export default App;
