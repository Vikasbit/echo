import { useAuth } from "../hooks/useAuth";
import { Loader2, Mail } from "lucide-react";
import { Link, Navigate } from "react-router-dom";
import { useState } from "react";
import { supabase } from "../lib/supabase";

export function VerifyEmail() {
  const { user, loading } = useAuth();
  const [resending, setResending] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  // If user is not logged in, they can't verify
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // If already verified, go to app
  if (user.email_confirmed_at) {
    return <Navigate to="/app" replace />;
  }

  const handleResend = async () => {
    setResending(true);
    setError("");
    setMessage("");
    
    if (!user.email) return;
    
    const { error } = await supabase.auth.resend({
      type: 'signup',
      email: user.email,
    });

    if (error) {
      setError(error.message);
    } else {
      setMessage("Verification email sent! Please check your inbox.");
    }
    setResending(false);
  };

  return (
    <div className="min-h-screen bg-background flex flex-col justify-center py-12 sm:px-6 lg:px-8 relative overflow-hidden">
      <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-primary/20 rounded-full blur-3xl opacity-50 mix-blend-screen pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-96 h-96 bg-secondary/30 rounded-full blur-3xl opacity-50 mix-blend-screen pointer-events-none" />

      <div className="sm:mx-auto sm:w-full sm:max-w-md relative z-10">
        <div className="glass-panel py-10 px-4 sm:rounded-2xl sm:px-10 shadow-2xl text-center">
          <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-6">
            <Mail className="w-8 h-8 text-primary" />
          </div>
          
          <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
            Verify your email
          </h2>
          
          <p className="text-muted-foreground mb-8">
            We sent a verification link to <span className="font-medium text-foreground">{user.email}</span>. 
            Please check your inbox to verify your account and access your workspace.
          </p>

          {error && (
            <div className="bg-destructive/10 border border-destructive/20 text-destructive text-sm p-3 rounded-lg mb-6">
              {error}
            </div>
          )}

          {message && (
            <div className="bg-green-500/10 border border-green-500/20 text-green-500 text-sm p-3 rounded-lg mb-6">
              {message}
            </div>
          )}

          <div className="space-y-4">
            <button
              onClick={handleResend}
              disabled={resending}
              className="w-full flex justify-center py-2.5 px-4 border border-border rounded-lg shadow-sm text-sm font-medium text-foreground bg-background hover:bg-muted/50 transition-all disabled:opacity-50"
            >
              {resending ? <Loader2 className="w-5 h-5 animate-spin" /> : "Resend Verification Email"}
            </button>
            
            <Link to="/login" className="block text-sm text-primary hover:text-primary/80">
              Back to login
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
