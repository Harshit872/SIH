import { useState } from "react";
import { Link, useNavigate } from "react-router";
import { Button } from "../../components/ui/button";

export function Login() {
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      navigate("/voyage-requirement-input");
    }, 1200);
  };

  const handleDemoAccess = () => {
    navigate("/voyage-requirement-input");
  };

  return (
    <div className="w-full">
      <div className="mb-8">
        <h2 className="text-3xl font-bold tracking-tight text-slate-900 mb-2">Welcome back</h2>
        <p className="text-slate-500 text-sm">
          Enter your credentials to access the intelligence platform.
        </p>
      </div>

      <form onSubmit={handleLogin} className="space-y-6">
        <div className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="email" className="text-sm font-medium leading-none text-slate-900">
              Email Address
            </label>
            <input
              id="email"
              type="email"
              placeholder="name@company.com"
              required
              className="flex h-11 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-all"
            />
          </div>
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label htmlFor="password" className="text-sm font-medium leading-none text-slate-900">
                Password
              </label>
              <a href="#" className="text-sm font-medium text-blue-600 hover:text-blue-700 hover:underline transition-colors">
                Forgot password?
              </a>
            </div>
            <input
              id="password"
              type="password"
              required
              className="flex h-11 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-all"
            />
          </div>
        </div>

        <Button type="submit" className="w-full h-11 text-base font-medium bg-blue-600 hover:bg-blue-700 text-white shadow-sm transition-all" disabled={isLoading}>
          {isLoading ? "Authenticating..." : "Sign in"}
        </Button>
      </form>

      <div className="relative my-8">
        <div className="absolute inset-0 flex items-center">
          <span className="w-full border-t border-slate-200" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-white px-3 text-slate-500 font-medium">
            Or continue with
          </span>
        </div>
      </div>

      <div className="grid gap-4">
        <Button variant="outline" type="button" onClick={handleDemoAccess} className="h-11 font-medium border-slate-200 text-slate-700 hover:bg-slate-50">
          Demo Access (No Account Required)
        </Button>
      </div>

      <p className="mt-8 text-center text-sm text-slate-500">
        Don't have an account?{" "}
        <Link to="/signup" className="font-medium text-blue-600 hover:text-blue-700 hover:underline transition-colors">
          Request access
        </Link>
      </p>
    </div>
  );
}
