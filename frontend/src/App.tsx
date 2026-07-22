import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AppLayout } from "./components/layout/AppLayout";
import { Documents } from "./pages/Documents";
import { Chat } from "./pages/Chat";
import { LandingPage } from "./pages/LandingPage";
import { Login } from "./pages/Login";
import { Register } from "./pages/Register";
import { ForgotPassword } from "./pages/ForgotPassword";
import { VerifyEmail } from "./pages/VerifyEmail";
import { AuthProvider } from "./hooks/useAuth";
import { ProtectedRoute } from "./components/layout/ProtectedRoute";

// Temporary placeholder components for other routes
const Dashboard = () => (
  <div className="flex flex-col gap-4">
    <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
    <div className="glass-panel rounded-xl p-6 h-64 flex items-center justify-center border-dashed">
      <p className="text-muted-foreground">Dashboard content will go here</p>
    </div>
  </div>
);

const Equipment = () => (
  <div className="flex flex-col gap-4">
    <h1 className="text-3xl font-bold tracking-tight">Equipment</h1>
    <div className="glass-panel rounded-xl p-6 h-64 flex items-center justify-center border-dashed">
      <p className="text-muted-foreground">Equipment registry will go here</p>
    </div>
  </div>
);

const Graph = () => (
  <div className="flex flex-col gap-4">
    <h1 className="text-3xl font-bold tracking-tight">Knowledge Graph</h1>
    <div className="glass-panel rounded-xl p-6 h-[600px] flex items-center justify-center border-dashed">
      <p className="text-muted-foreground">Graph visualization will go here</p>
    </div>
  </div>
);

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public marketing page */}
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/verify-email" element={<VerifyEmail />} />

          {/* Authenticated app routes */}
          <Route path="/app" element={
            <ProtectedRoute>
              <AppLayout />
            </ProtectedRoute>
          }>
            <Route index element={<Dashboard />} />
            <Route path="chat" element={<Chat />} />
            <Route path="documents" element={<Documents />} />
            <Route path="equipment" element={<Equipment />} />
            <Route path="graph" element={<Graph />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
