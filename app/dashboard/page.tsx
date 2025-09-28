"use client"

import { useState, useEffect } from "react"
import { useSession } from "next-auth/react"
import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import {
  MessageSquare,
  Sprout,
  Shield,
  TrendingUp,
  Cloud,
  Droplets,
  Bug,
  BarChart3,
  ArrowRight,
  Activity,
  Calendar,
  Bell,
  Star,
} from "lucide-react"

const quickActions = [
  {
    title: "Ask AI Assistant",
    description: "Get instant farming advice",
    icon: MessageSquare,
    href: "/dashboard/chat",
    color: "bg-blue-500",
  },
  {
    title: "Detect Disease",
    description: "Upload crop image for analysis",
    icon: Shield,
    href: "/dashboard/agents/disease-detection",
    color: "bg-red-500",
  },
  {
    title: "Weather Forecast",
    description: "Check agricultural advisory",
    icon: Cloud,
    href: "/dashboard/agents/weather",
    color: "bg-orange-500",
  },
  {
    title: "Market Prices",
    description: "Live commodity rates",
    icon: TrendingUp,
    href: "/dashboard/agents/market-prices",
    color: "bg-green-500",
  },
]

const features = [
  {
    title: "Crop Recommendations",
    description: "Get personalized crop suggestions based on your soil and climate conditions",
    icon: Sprout,
    href: "/dashboard/agents/crop-recommendation",
  },
  {
    title: "Pest Management",
    description: "Identify and control pests with expert guidance",
    icon: Bug,
    href: "/dashboard/agents/pest-control",
  },
  {
    title: "Irrigation Planning",
    description: "Optimize water usage with smart irrigation schedules",
    icon: Droplets,
    href: "/dashboard/agents/irrigation",
  },
  {
    title: "Fertilizer Guide",
    description: "Get nutrition recommendations for better yields",
    icon: BarChart3,
    href: "/dashboard/agents/fertilizer",
  },
]

const recentActivity = [
  {
    id: 1,
    type: "query",
    title: "Asked about tomato fertilizer",
    time: "2 hours ago",
    status: "completed",
  },
  {
    id: 2,
    type: "detection",
    title: "Disease detection on wheat crop",
    time: "5 hours ago",
    status: "completed",
  },
  {
    id: 3,
    type: "recommendation",
    title: "Received crop recommendations",
    time: "1 day ago",
    status: "completed",
  },
]

const upcomingTasks = [
  {
    id: 1,
    title: "Apply fertilizer to wheat field",
    date: "Tomorrow",
    priority: "high",
  },
  {
    id: 2,
    title: "Check weather forecast for irrigation",
    date: "In 2 days",
    priority: "medium",
  },
  {
    id: 3,
    title: "Monitor pest activity",
    date: "This weekend",
    priority: "low",
  },
]

export default function DashboardPage() {
  const { data: session } = useSession()

  const [greeting, setGreeting] = useState("Good day")

  useEffect(() => {
    const hour = new Date().getHours()
    if (hour < 12) setGreeting("Good morning")
    else if (hour < 17) setGreeting("Good afternoon")
    else setGreeting("Good evening")
  }, [])

  return (
    <div className="p-6 space-y-6">
      {/* Welcome Section */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">
          {greeting}, {session?.user?.name?.split(' ')[0] || 'Farmer'}! 👋
        </h1>
        <p className="text-muted-foreground">
          Welcome to your agricultural dashboard. How can we help you grow better today?
        </p>
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickActions.map((action) => (
            <Link key={action.title} href={action.href}>
              <Card className="feature-card group">
                <CardContent className="p-4">
                  <div className="flex items-center space-x-3">
                    <div className={`p-3 rounded-lg ${action.color} text-white`}>
                      <action.icon className="h-6 w-6" />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-semibold">{action.title}</h3>
                      <p className="text-sm text-muted-foreground">{action.description}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      </div>

      {/* Dashboard Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* AI Features */}
        <div className="lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">AI-Powered Features</h2>
            <Link href="/dashboard/agents">
              <Button variant="ghost" size="sm">
                View all <ArrowRight className="ml-1 h-4 w-4" />
              </Button>
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {features.map((feature) => (
              <Link key={feature.title} href={feature.href}>
                <Card className="feature-card">
                  <CardHeader className="pb-3">
                    <div className="flex items-center space-x-3">
                      <div className="p-2 bg-agricultural-100 rounded-lg text-agricultural-600">
                        <feature.icon className="h-5 w-5" />
                      </div>
                      <CardTitle className="text-lg">{feature.title}</CardTitle>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <CardDescription>{feature.description}</CardDescription>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Weather Widget */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center space-x-2">
                <Cloud className="h-5 w-5" />
                <span>Today's Weather</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span>Temperature</span>
                  <span className="font-medium">28°C</span>
                </div>
                <div className="flex justify-between">
                  <span>Humidity</span>
                  <span className="font-medium">65%</span>
                </div>
                <div className="flex justify-between">
                  <span>Rain Chance</span>
                  <span className="font-medium">20%</span>
                </div>
                <Link href="/dashboard/agents/weather">
                  <Button className="w-full mt-3" variant="outline" size="sm">
                    View Forecast
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>

          {/* Market Prices */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center space-x-2">
                <TrendingUp className="h-5 w-5" />
                <span>Market Prices</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span>Wheat</span>
                  <span className="font-medium text-green-600">₹2,150/quintal</span>
                </div>
                <div className="flex justify-between">
                  <span>Rice</span>
                  <span className="font-medium text-green-600">₹1,850/quintal</span>
                </div>
                <div className="flex justify-between">
                  <span>Tomato</span>
                  <span className="font-medium text-red-600">₹45/kg</span>
                </div>
                <Link href="/dashboard/agents/market-prices">
                  <Button className="w-full mt-3" variant="outline" size="sm">
                    View All Prices
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Recent Activity & Tasks */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Activity className="h-5 w-5" />
              <span>Recent Activity</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {recentActivity.map((activity) => (
                <div key={activity.id} className="flex items-center space-x-3 p-2 rounded-lg hover:bg-muted/50">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <div className="flex-1">
                    <p className="text-sm font-medium">{activity.title}</p>
                    <p className="text-xs text-muted-foreground">{activity.time}</p>
                  </div>
                </div>
              ))}
              <Link href="/dashboard/history">
                <Button variant="ghost" size="sm" className="w-full">
                  View all activity
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>

        {/* Upcoming Tasks */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Calendar className="h-5 w-5" />
              <span>Upcoming Tasks</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {upcomingTasks.map((task) => (
                <div key={task.id} className="flex items-center space-x-3 p-2 rounded-lg hover:bg-muted/50">
                  <div className={`w-2 h-2 rounded-full ${
                    task.priority === 'high' ? 'bg-red-500' :
                    task.priority === 'medium' ? 'bg-yellow-500' : 'bg-blue-500'
                  }`}></div>
                  <div className="flex-1">
                    <p className="text-sm font-medium">{task.title}</p>
                    <p className="text-xs text-muted-foreground">{task.date}</p>
                  </div>
                </div>
              ))}
              <Link href="/dashboard/calendar">
                <Button variant="ghost" size="sm" className="w-full">
                  View calendar
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tips & Recommendations */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Star className="h-5 w-5" />
            <span>Today's Farming Tips</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-agricultural-50 rounded-lg">
              <h4 className="font-semibold text-agricultural-800 mb-2">Irrigation Tip</h4>
              <p className="text-sm text-agricultural-600">
                Water your crops early morning to reduce water loss through evaporation.
              </p>
            </div>
            <div className="p-4 bg-blue-50 rounded-lg">
              <h4 className="font-semibold text-blue-800 mb-2">Weather Alert</h4>
              <p className="text-sm text-blue-600">
                Light rain expected tomorrow. Good time for sowing if soil conditions are right.
              </p>
            </div>
            <div className="p-4 bg-orange-50 rounded-lg">
              <h4 className="font-semibold text-orange-800 mb-2">Market Insight</h4>
              <p className="text-sm text-orange-600">
                Tomato prices are rising. Consider harvesting and selling your ready crops.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
