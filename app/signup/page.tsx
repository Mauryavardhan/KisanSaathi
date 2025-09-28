"use client"

import { useState } from "react"
import { signIn } from "next-auth/react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Sprout, Eye, EyeOff, Mail, Lock, User, MapPin, Phone } from "lucide-react"
import toast from "react-hot-toast"

export default function SignUpPage() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
    phone: "",
    location: "",
  })
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!formData.name || !formData.email || !formData.password) {
      toast.error("Please fill in all required fields")
      return
    }

    if (formData.password !== formData.confirmPassword) {
      toast.error("Passwords do not match")
      return
    }

    if (formData.password.length < 6) {
      toast.error("Password must be at least 6 characters")
      return
    }

    setIsLoading(true)
    
    try {
      const response = await fetch("/api/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: formData.name,
          email: formData.email,
          password: formData.password,
          phone: formData.phone,
          location: formData.location,
        }),
      })

      if (response.ok) {
        toast.success("Account created successfully!")
        // Auto sign in after successful registration
        const result = await signIn("credentials", {
          email: formData.email,
          password: formData.password,
          redirect: false,
        })
        
        if (result?.ok) {
          router.push("/dashboard")
        }
      } else {
        const data = await response.json()
        toast.error(data.message || "Failed to create account")
      }
    } catch (error) {
      toast.error("Something went wrong. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  const handleGoogleSignIn = async () => {
    toast.info("Google Sign-in coming soon! Please use email/password for now.")
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-agricultural-50 to-earth-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-flex items-center space-x-2">
            <Sprout className="h-10 w-10 text-agricultural-600" />
            <span className="text-2xl font-bold text-agricultural-800">Kisan Saathi</span>
          </Link>
          <p className="text-muted-foreground mt-2">Join thousands of farmers using AI</p>
        </div>

        <Card>
          <CardHeader className="text-center">
            <CardTitle>Create Account</CardTitle>
            <CardDescription>
              Start your journey with Kisan Saathi today
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Input
                  type="text"
                  name="name"
                  placeholder="Full name"
                  value={formData.name}
                  onChange={handleChange}
                  startIcon={<User className="h-4 w-4" />}
                  required
                />
              </div>

              <div>
                <Input
                  type="email"
                  name="email"
                  placeholder="Email address"
                  value={formData.email}
                  onChange={handleChange}
                  startIcon={<Mail className="h-4 w-4" />}
                  required
                />
              </div>

              <div>
                <Input
                  type="tel"
                  name="phone"
                  placeholder="Phone number (optional)"
                  value={formData.phone}
                  onChange={handleChange}
                  startIcon={<Phone className="h-4 w-4" />}
                />
              </div>

              <div>
                <Input
                  type="text"
                  name="location"
                  placeholder="Location (optional)"
                  value={formData.location}
                  onChange={handleChange}
                  startIcon={<MapPin className="h-4 w-4" />}
                />
              </div>
              
              <div>
                <Input
                  type={showPassword ? "text" : "password"}
                  name="password"
                  placeholder="Password"
                  value={formData.password}
                  onChange={handleChange}
                  startIcon={<Lock className="h-4 w-4" />}
                  endIcon={
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="text-muted-foreground hover:text-foreground"
                    >
                      {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                  }
                  required
                />
              </div>

              <div>
                <Input
                  type={showConfirmPassword ? "text" : "password"}
                  name="confirmPassword"
                  placeholder="Confirm password"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  startIcon={<Lock className="h-4 w-4" />}
                  endIcon={
                    <button
                      type="button"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                      className="text-muted-foreground hover:text-foreground"
                    >
                      {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                  }
                  required
                />
              </div>

              <div className="text-xs text-muted-foreground">
                By creating an account, you agree to our{" "}
                <Link href="/terms" className="text-agricultural-600 hover:underline">
                  Terms of Service
                </Link>{" "}
                and{" "}
                <Link href="/privacy" className="text-agricultural-600 hover:underline">
                  Privacy Policy
                </Link>
              </div>

              <Button 
                type="submit" 
                className="w-full bg-agricultural-600 hover:bg-agricultural-700"
                loading={isLoading}
                disabled={isLoading}
              >
                Create Account
              </Button>
            </form>

            <div className="mt-6">
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-muted" />
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="bg-background px-2 text-muted-foreground">Or continue with</span>
                </div>
              </div>

              <Button
                type="button"
                variant="outline"
                className="w-full mt-4"
                onClick={handleGoogleSignIn}
                disabled={isLoading}
              >
                <svg className="w-4 h-4 mr-2" viewBox="0 0 24 24">
                  <path
                    fill="currentColor"
                    d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                  />
                  <path
                    fill="currentColor"
                    d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                  />
                  <path
                    fill="currentColor"
                    d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                  />
                  <path
                    fill="currentColor"
                    d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                  />
                </svg>
                Continue with Google
              </Button>
            </div>

            <div className="mt-6 text-center text-sm">
              <span className="text-muted-foreground">Already have an account? </span>
              <Link href="/signin" className="text-agricultural-600 hover:underline font-medium">
                Sign in
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
