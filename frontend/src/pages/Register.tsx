import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Lock, Mail, User, Building, Loader2, ChevronRight, ChevronLeft, ArrowRight } from "lucide-react";
import { supabase } from "../lib/supabase";

const INDUSTRIES = [
  "Manufacturing", "Automotive", "Data Center", 
  "Power Plant", "Chemical", "Healthcare", 
  "Logistics", "Others"
];

const COMPANY_SIZES = [
  "1-10", "11-50", "51-250", "250+"
];

export function Register() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Step 1: Personal Info
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  // Step 2: Company Info
  const [companyName, setCompanyName] = useState("");
  const [industry, setIndustry] = useState("");
  const [companySize, setCompanySize] = useState("");

  const handleNextStep = () => {
    setError("");
    if (step === 1) {
      if (!fullName || !email || !password || !confirmPassword) {
        setError("Please fill out all fields");
        return;
      }
      if (password !== confirmPassword) {
        setError("Passwords do not match");
        return;
      }
      if (password.length < 8) {
        setError("Password must be at least 8 characters long");
        return;
      }
      setStep(2);
    } else if (step === 2) {
      if (!companyName || !industry || !companySize) {
        setError("Please fill out all fields");
        return;
      }
      setStep(3);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          full_name: fullName,
          company_name: companyName,
          industry: industry,
          company_size: companySize,
        }
      }
    });

    if (error) {
      setError(error.message);
      setLoading(false);
      setStep(1); // Go back if error is related to email/password
    } else {
      navigate("/app");
    }
  };

  return (
    <div className="min-h-screen bg-background flex flex-col justify-center py-12 sm:px-6 lg:px-8 relative overflow-hidden">
      <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-primary/20 rounded-full blur-3xl opacity-50 mix-blend-screen pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-96 h-96 bg-secondary/30 rounded-full blur-3xl opacity-50 mix-blend-screen pointer-events-none" />

      <div className="sm:mx-auto sm:w-full sm:max-w-md relative z-10">
        <h2 className="mt-2 text-center text-3xl font-bold tracking-tight text-foreground">
          Create an enterprise account
        </h2>
        <p className="mt-2 text-center text-sm text-muted-foreground">
          Already have an account?{" "}
          <Link to="/login" className="font-medium text-primary hover:text-primary/80 transition-colors">
            Sign in
          </Link>
        </p>

        {/* Step Indicators */}
        <div className="mt-8 flex justify-center items-center space-x-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="flex items-center">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-colors ${
                step === i ? "bg-primary text-primary-foreground" : 
                step > i ? "bg-primary/50 text-white" : "bg-white/10 text-muted-foreground"
              }`}>
                {i}
              </div>
              {i < 3 && <div className={`w-12 h-1 ${step > i ? "bg-primary/50" : "bg-white/10"}`} />}
            </div>
          ))}
        </div>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md relative z-10">
        <div className="glass-panel py-8 px-4 sm:rounded-2xl sm:px-10 shadow-2xl">
          <form className="space-y-6" onSubmit={(e) => { e.preventDefault(); if (step === 3) handleRegister(e); }}>
            {error && (
              <div className="bg-destructive/10 border border-destructive/20 text-destructive text-sm p-3 rounded-lg flex items-center">
                {error}
              </div>
            )}
            
            {step === 1 && (
              <div className="space-y-4 animate-in fade-in slide-in-from-right-4">
                <h3 className="text-lg font-medium text-foreground">Personal Information</h3>
                <div>
                  <label className="block text-sm font-medium text-foreground">Full Name</label>
                  <div className="mt-1 relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <User className="h-5 w-5 text-muted-foreground" />
                    </div>
                    <input type="text" required value={fullName} onChange={(e) => setFullName(e.target.value)}
                      className="block w-full pl-10 pr-3 py-2 border border-border rounded-lg bg-background/50 text-foreground focus:ring-2 focus:ring-primary focus:border-transparent transition-all sm:text-sm"
                      placeholder="John Doe" />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground">Work Email</label>
                  <div className="mt-1 relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <Mail className="h-5 w-5 text-muted-foreground" />
                    </div>
                    <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)}
                      className="block w-full pl-10 pr-3 py-2 border border-border rounded-lg bg-background/50 text-foreground focus:ring-2 focus:ring-primary focus:border-transparent transition-all sm:text-sm"
                      placeholder="you@company.com" />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground">Password</label>
                  <div className="mt-1 relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <Lock className="h-5 w-5 text-muted-foreground" />
                    </div>
                    <input type="password" required value={password} onChange={(e) => setPassword(e.target.value)}
                      className="block w-full pl-10 pr-3 py-2 border border-border rounded-lg bg-background/50 text-foreground focus:ring-2 focus:ring-primary focus:border-transparent transition-all sm:text-sm"
                      placeholder="••••••••" />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground">Confirm Password</label>
                  <div className="mt-1 relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <Lock className="h-5 w-5 text-muted-foreground" />
                    </div>
                    <input type="password" required value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)}
                      className="block w-full pl-10 pr-3 py-2 border border-border rounded-lg bg-background/50 text-foreground focus:ring-2 focus:ring-primary focus:border-transparent transition-all sm:text-sm"
                      placeholder="••••••••" />
                  </div>
                </div>

                <div className="pt-4">
                  <button type="button" onClick={handleNextStep}
                    className="w-full flex justify-center items-center py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-primary-foreground bg-primary hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary focus:ring-offset-background transition-all">
                    Continue <ChevronRight className="ml-2 w-4 h-4" />
                  </button>
                </div>
              </div>
            )}

            {step === 2 && (
              <div className="space-y-4 animate-in fade-in slide-in-from-right-4">
                <div className="flex items-center gap-2 mb-4">
                  <button type="button" onClick={() => setStep(1)} className="p-1 rounded-full hover:bg-white/10 transition-colors">
                    <ChevronLeft className="w-5 h-5 text-muted-foreground" />
                  </button>
                  <h3 className="text-lg font-medium text-foreground">Company Information</h3>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground">Company Name</label>
                  <div className="mt-1 relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <Building className="h-5 w-5 text-muted-foreground" />
                    </div>
                    <input type="text" required value={companyName} onChange={(e) => setCompanyName(e.target.value)}
                      className="block w-full pl-10 pr-3 py-2 border border-border rounded-lg bg-background/50 text-foreground focus:ring-2 focus:ring-primary focus:border-transparent transition-all sm:text-sm"
                      placeholder="Acme Corp" />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground">Industry</label>
                  <div className="mt-1">
                    <select required value={industry} onChange={(e) => setIndustry(e.target.value)}
                      className="block w-full px-3 py-2 border border-border rounded-lg bg-background/50 text-foreground focus:ring-2 focus:ring-primary focus:border-transparent transition-all sm:text-sm">
                      <option value="" disabled>Select an industry</option>
                      {INDUSTRIES.map(ind => <option key={ind} value={ind}>{ind}</option>)}
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground">Company Size (Employees)</label>
                  <div className="mt-1">
                    <select required value={companySize} onChange={(e) => setCompanySize(e.target.value)}
                      className="block w-full px-3 py-2 border border-border rounded-lg bg-background/50 text-foreground focus:ring-2 focus:ring-primary focus:border-transparent transition-all sm:text-sm">
                      <option value="" disabled>Select company size</option>
                      {COMPANY_SIZES.map(size => <option key={size} value={size}>{size}</option>)}
                    </select>
                  </div>
                </div>

                <div className="pt-4">
                  <button type="button" onClick={handleNextStep}
                    className="w-full flex justify-center items-center py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-primary-foreground bg-primary hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary focus:ring-offset-background transition-all">
                    Continue <ChevronRight className="ml-2 w-4 h-4" />
                  </button>
                </div>
              </div>
            )}

            {step === 3 && (
              <div className="space-y-4 animate-in fade-in slide-in-from-right-4">
                <div className="flex items-center gap-2 mb-4">
                  <button type="button" onClick={() => setStep(2)} className="p-1 rounded-full hover:bg-white/10 transition-colors">
                    <ChevronLeft className="w-5 h-5 text-muted-foreground" />
                  </button>
                  <h3 className="text-lg font-medium text-foreground">Workspace Setup</h3>
                </div>

                <div className="bg-primary/10 border border-primary/20 rounded-xl p-6 text-center">
                  <Building className="w-12 h-12 text-primary mx-auto mb-4" />
                  <h4 className="text-xl font-bold text-foreground">{companyName} Workspace</h4>
                  <p className="text-sm text-muted-foreground mt-2">
                    We will automatically provision a secure, isolated workspace for your team with default AI settings.
                  </p>
                </div>

                <div className="pt-4">
                  <button type="submit" disabled={loading}
                    className="w-full flex justify-center items-center py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-primary-foreground bg-primary hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary focus:ring-offset-background transition-all disabled:opacity-50">
                    {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <>Create Workspace <ArrowRight className="ml-2 w-4 h-4" /></>}
                  </button>
                </div>
              </div>
            )}
          </form>
        </div>
      </div>
    </div>
  );
}
