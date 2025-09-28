import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { 
  Sprout, 
  Shield, 
  TrendingUp, 
  Cloud, 
  MessageCircle, 
  Leaf,
  Users,
  Award,
  ArrowRight,
  Phone,
  Mail
} from "lucide-react"

const features = [
  {
    icon: <MessageCircle className="h-8 w-8" />,
    title: "AI Chat Assistant",
    description: "Get instant answers to your farming questions in your preferred language with our advanced AI."
  },
  {
    icon: <Sprout className="h-8 w-8" />,
    title: "Crop Recommendations",
    description: "Receive personalized crop suggestions based on your soil, climate, and market conditions."
  },
  {
    icon: <Shield className="h-8 w-8" />,
    title: "Disease Detection",
    description: "Upload images of your crops to identify diseases and get treatment recommendations."
  },
  {
    icon: <TrendingUp className="h-8 w-8" />,
    title: "Market Insights",
    description: "Access real-time market prices and trends to make informed selling decisions."
  },
  {
    icon: <Cloud className="h-8 w-8" />,
    title: "Weather Advisory",
    description: "Get accurate weather forecasts and agricultural advisories for your location."
  },
  {
    icon: <Leaf className="h-8 w-8" />,
    title: "Sustainable Farming",
    description: "Learn eco-friendly farming practices to improve yield while protecting the environment."
  }
]

const stats = [
  { value: "50K+", label: "Farmers Helped" },
  { value: "100K+", label: "Queries Resolved" },
  { value: "95%", label: "Satisfaction Rate" },
  { value: "24/7", label: "AI Support" }
]

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-agricultural-50 to-earth-50">
      {/* Navigation */}
      <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center space-x-2">
              <Sprout className="h-8 w-8 text-agricultural-600" />
              <span className="text-xl font-bold text-agricultural-800">Kisan Saathi</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/signin">
                <Button variant="ghost">Sign In</Button>
              </Link>
              <Link href="/signup">
                <Button className="bg-agricultural-600 hover:bg-agricultural-700">
                  Get Started
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="py-20 text-center">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-4xl">
            <h1 className="heading-xl text-agricultural-900 mb-6">
              Empowering Farmers with{" "}
              <span className="text-agricultural-600">AI Technology</span>
            </h1>
            <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
              Kisan Saathi is your intelligent farming companion, providing personalized advice, 
              crop recommendations, and real-time agricultural insights to boost your productivity.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/signup">
                <Button size="xl" className="bg-agricultural-600 hover:bg-agricultural-700">
                  Start Farming Smarter
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/demo">
                <Button size="xl" variant="outline">
                  Watch Demo
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-agricultural-600 text-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            {stats.map((stat, index) => (
              <div key={index}>
                <div className="text-3xl md:text-4xl font-bold mb-2">{stat.value}</div>
                <div className="text-agricultural-100">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="heading-lg text-agricultural-900 mb-4">
              Comprehensive Agricultural Solutions
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Our AI-powered platform offers everything you need to make informed farming decisions
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="feature-card">
                <CardHeader>
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-agricultural-100 rounded-lg text-agricultural-600">
                      {feature.icon}
                    </div>
                    <CardTitle className="text-lg">{feature.title}</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-muted/50">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="heading-lg text-agricultural-900 mb-4">
              How Kisan Saathi Works
            </h2>
            <p className="text-xl text-muted-foreground">
              Simple steps to get the agricultural guidance you need
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="mx-auto w-16 h-16 bg-agricultural-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mb-4">
                1
              </div>
              <h3 className="text-xl font-semibold mb-2">Ask Your Question</h3>
              <p className="text-muted-foreground">
                Type, speak, or upload images to ask any farming-related question
              </p>
            </div>
            <div className="text-center">
              <div className="mx-auto w-16 h-16 bg-agricultural-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mb-4">
                2
              </div>
              <h3 className="text-xl font-semibold mb-2">AI Analysis</h3>
              <p className="text-muted-foreground">
                Our AI processes your query using advanced agricultural knowledge
              </p>
            </div>
            <div className="text-center">
              <div className="mx-auto w-16 h-16 bg-agricultural-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mb-4">
                3
              </div>
              <h3 className="text-xl font-semibold mb-2">Get Solutions</h3>
              <p className="text-muted-foreground">
                Receive personalized recommendations and actionable insights
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-agricultural-gradient text-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="heading-lg mb-4">
            Ready to Transform Your Farming?
          </h2>
          <p className="text-xl text-agricultural-100 mb-8 max-w-2xl mx-auto">
            Join thousands of farmers who are already using Kisan Saathi to improve their yields and profits
          </p>
          <Link href="/signup">
            <Button size="xl" variant="secondary" className="bg-white text-agricultural-600 hover:bg-agricultural-50">
              Start Your Journey Today
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-agricultural-900 text-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <Sprout className="h-8 w-8" />
                <span className="text-xl font-bold">Kisan Saathi</span>
              </div>
              <p className="text-agricultural-300">
                Empowering farmers with AI-driven agricultural insights and recommendations.
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Features</h3>
              <ul className="space-y-2 text-agricultural-300">
                <li>AI Chat Assistant</li>
                <li>Crop Recommendations</li>
                <li>Disease Detection</li>
                <li>Market Insights</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Support</h3>
              <ul className="space-y-2 text-agricultural-300">
                <li>Help Center</li>
                <li>Documentation</li>
                <li>Contact Us</li>
                <li>Community</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Contact</h3>
              <div className="space-y-2 text-agricultural-300">
                <div className="flex items-center space-x-2">
                  <Mail className="h-4 w-4" />
                  <span>support@kisansaathi.com</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Phone className="h-4 w-4" />
                  <span>+91 98765 43210</span>
                </div>
              </div>
            </div>
          </div>
          <div className="border-t border-agricultural-800 mt-8 pt-8 text-center text-agricultural-400">
            <p>&copy; 2024 Kisan Saathi. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
