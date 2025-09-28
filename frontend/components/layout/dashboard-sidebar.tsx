"use client"

import { useState } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import {
  MessageSquare,
  Sprout,
  Shield,
  TrendingUp,
  Cloud,
  Droplets,
  Bug,
  Banknote,
  FileText,
  History,
  Settings,
  ChevronLeft,
  ChevronRight,
  Home,
  BarChart3,
  Calendar,
  Bell,
  HelpCircle,
} from "lucide-react"

const navigationItems = [
  {
    title: "Dashboard",
    href: "/dashboard",
    icon: Home,
    description: "Overview and quick actions"
  },
  {
    title: "Chat",
    href: "/dashboard/chat",
    icon: MessageSquare,
    description: "Ask farming questions"
  },
  {
    title: "Crop Advisor",
    href: "/dashboard/agents/crop-recommendation",
    icon: Sprout,
    description: "Get crop recommendations"
  },
  {
    title: "Disease Detective",
    href: "/dashboard/agents/disease-detection",
    icon: Shield,
    description: "Detect plant diseases"
  },
  {
    title: "Pest Control",
    href: "/dashboard/agents/pest-control",
    icon: Bug,
    description: "Pest management solutions"
  },
  {
    title: "Weather Insights",
    href: "/dashboard/agents/weather",
    icon: Cloud,
    description: "Weather forecasts & advisories"
  },
  {
    title: "Irrigation Planner",
    href: "/dashboard/agents/irrigation",
    icon: Droplets,
    description: "Water management guidance"
  },
  {
    title: "Market Prices",
    href: "/dashboard/agents/market-prices",
    icon: TrendingUp,
    description: "Live market rates"
  },
  {
    title: "Fertilizer Guide",
    href: "/dashboard/agents/fertilizer",
    icon: BarChart3,
    description: "Nutrition recommendations"
  },
  {
    title: "Govt Schemes",
    href: "/dashboard/agents/schemes",
    icon: Banknote,
    description: "Government benefits"
  },
  {
    title: "Farming Calendar",
    href: "/dashboard/calendar",
    icon: Calendar,
    description: "Seasonal planning"
  },
  {
    title: "News & Updates",
    href: "/dashboard/news",
    icon: Bell,
    description: "Agricultural news"
  },
]

const bottomItems = [
  {
    title: "Chat History",
    href: "/dashboard/history",
    icon: History,
    description: "Previous conversations"
  },
  {
    title: "Help & Support",
    href: "/dashboard/help",
    icon: HelpCircle,
    description: "Get assistance"
  },
  {
    title: "Settings",
    href: "/dashboard/settings",
    icon: Settings,
    description: "Account preferences"
  },
]

export function DashboardSidebar() {
  const [collapsed, setCollapsed] = useState(false)
  const pathname = usePathname()

  return (
    <div className={cn(
      "bg-card border-r transition-all duration-300 flex flex-col",
      collapsed ? "w-16" : "w-64"
    )}>
      {/* Header */}
      <div className="p-4 border-b">
        <div className="flex items-center justify-between">
          {!collapsed && (
            <div className="flex items-center space-x-2">
              <Sprout className="h-8 w-8 text-agricultural-600" />
              <span className="text-xl font-bold text-agricultural-800">Kisan Saathi</span>
            </div>
          )}
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="p-1 rounded-md hover:bg-accent"
          >
            {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
          </button>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
        {navigationItems.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center space-x-3 p-3 rounded-lg transition-colors group",
                isActive 
                  ? "bg-agricultural-100 text-agricultural-800 border border-agricultural-200" 
                  : "hover:bg-accent text-muted-foreground hover:text-foreground"
              )}
              title={collapsed ? item.title : undefined}
            >
              <item.icon className={cn(
                "h-5 w-5 flex-shrink-0",
                isActive ? "text-agricultural-600" : ""
              )} />
              {!collapsed && (
                <div className="flex-1 min-w-0">
                  <div className="font-medium">{item.title}</div>
                  <div className="text-xs text-muted-foreground truncate">
                    {item.description}
                  </div>
                </div>
              )}
            </Link>
          )
        })}
      </nav>

      {/* Bottom Navigation */}
      <div className="p-4 border-t space-y-2">
        {bottomItems.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center space-x-3 p-3 rounded-lg transition-colors",
                isActive 
                  ? "bg-agricultural-100 text-agricultural-800" 
                  : "hover:bg-accent text-muted-foreground hover:text-foreground"
              )}
              title={collapsed ? item.title : undefined}
            >
              <item.icon className={cn(
                "h-5 w-5 flex-shrink-0",
                isActive ? "text-agricultural-600" : ""
              )} />
              {!collapsed && (
                <span className="font-medium">{item.title}</span>
              )}
            </Link>
          )
        })}
      </div>
    </div>
  )
}
