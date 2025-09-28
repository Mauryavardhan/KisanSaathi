"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Sprout, MapPin, Thermometer, Droplets, BarChart3, TrendingUp } from "lucide-react"
import { api } from "@/lib/api"
import toast from "react-hot-toast"

interface CropRecommendation {
  name: string
  confidence: number
  reasons: string[]
  expected_yield: number
  market_price: number
}

const soilTypes = [
  { value: "loamy", label: "Loamy" },
  { value: "clay", label: "Clay" },
  { value: "sandy", label: "Sandy" },
  { value: "silty", label: "Silty" },
  { value: "black", label: "Black Cotton" },
  { value: "red", label: "Red" },
  { value: "alluvial", label: "Alluvial" }
]

const seasons = [
  { value: "kharif", label: "Kharif (Summer)" },
  { value: "rabi", label: "Rabi (Winter)" },
  { value: "zaid", label: "Zaid (Summer)" }
]

export default function CropRecommendationPage() {
  const [formData, setFormData] = useState({
    soil_type: "",
    ph_level: "",
    nitrogen: "",
    phosphorus: "",
    potassium: "",
    location: "",
    season: "",
    previous_crop: ""
  })
  const [recommendations, setRecommendations] = useState<CropRecommendation[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [showResults, setShowResults] = useState(false)

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!formData.soil_type || !formData.location) {
      toast.error("Please fill in required fields")
      return
    }

    setIsLoading(true)
    try {
      const response = await api.getCropRecommendation({
        soil_type: formData.soil_type,
        ph_level: formData.ph_level ? parseFloat(formData.ph_level) : undefined,
        nitrogen: formData.nitrogen ? parseFloat(formData.nitrogen) : undefined,
        phosphorus: formData.phosphorus ? parseFloat(formData.phosphorus) : undefined,
        potassium: formData.potassium ? parseFloat(formData.potassium) : undefined,
        location: formData.location,
        season: formData.season || undefined,
        previous_crop: formData.previous_crop || undefined
      })

      setRecommendations(response.recommended_crops)
      setShowResults(true)
      toast.success("Crop recommendations generated!")
    } catch (error) {
      console.error("Error getting recommendations:", error)
      // Fallback with sample data
      const sampleRecommendations: CropRecommendation[] = [
        {
          name: "Wheat",
          confidence: 0.92,
          reasons: ["Suitable soil type", "Optimal season", "Good market demand"],
          expected_yield: 4.2,
          market_price: 2150
        },
        {
          name: "Barley",
          confidence: 0.87,
          reasons: ["Compatible with soil pH", "Low water requirement", "Drought resistant"],
          expected_yield: 3.8,
          market_price: 1950
        },
        {
          name: "Mustard",
          confidence: 0.83,
          reasons: ["Suitable for rotation", "Good oil content", "Market demand"],
          expected_yield: 1.5,
          market_price: 5200
        }
      ]
      setRecommendations(sampleRecommendations)
      setShowResults(true)
      toast.success("Showing sample recommendations (backend not connected)")
    } finally {
      setIsLoading(false)
    }
  }

  const resetForm = () => {
    setFormData({
      soil_type: "",
      ph_level: "",
      nitrogen: "",
      phosphorus: "",
      potassium: "",
      location: "",
      season: "",
      previous_crop: ""
    })
    setShowResults(false)
    setRecommendations([])
  }

  return (
    <div className="p-6 space-y-6">
      <div className="space-y-2">
        <h1 className="text-2xl font-bold flex items-center space-x-2">
          <Sprout className="h-8 w-8 text-agricultural-600" />
          <span>Crop Recommendation</span>
        </h1>
        <p className="text-muted-foreground">
          Get personalized crop suggestions based on your soil and environmental conditions
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <Card>
          <CardHeader>
            <CardTitle>Field Information</CardTitle>
            <CardDescription>
              Provide details about your field conditions for accurate recommendations
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="location">Location *</Label>
                <Input
                  id="location"
                  placeholder="Enter your location (city, state)"
                  value={formData.location}
                  onChange={(e) => handleInputChange("location", e.target.value)}
                  startIcon={<MapPin className="h-4 w-4" />}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="soil_type">Soil Type *</Label>
                <Select
                  value={formData.soil_type}
                  onValueChange={(value) => handleInputChange("soil_type", value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select soil type" />
                  </SelectTrigger>
                  <SelectContent>
                    {soilTypes.map((soil) => (
                      <SelectItem key={soil.value} value={soil.value}>
                        {soil.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="season">Season</Label>
                <Select
                  value={formData.season}
                  onValueChange={(value) => handleInputChange("season", value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select season" />
                  </SelectTrigger>
                  <SelectContent>
                    {seasons.map((season) => (
                      <SelectItem key={season.value} value={season.value}>
                        {season.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="ph_level">pH Level</Label>
                  <Input
                    id="ph_level"
                    type="number"
                    step="0.1"
                    min="0"
                    max="14"
                    placeholder="6.5"
                    value={formData.ph_level}
                    onChange={(e) => handleInputChange("ph_level", e.target.value)}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="previous_crop">Previous Crop</Label>
                  <Input
                    id="previous_crop"
                    placeholder="e.g., Paddy"
                    value={formData.previous_crop}
                    onChange={(e) => handleInputChange("previous_crop", e.target.value)}
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="nitrogen">Nitrogen (kg/ha)</Label>
                  <Input
                    id="nitrogen"
                    type="number"
                    placeholder="120"
                    value={formData.nitrogen}
                    onChange={(e) => handleInputChange("nitrogen", e.target.value)}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="phosphorus">Phosphorus (kg/ha)</Label>
                  <Input
                    id="phosphorus"
                    type="number"
                    placeholder="60"
                    value={formData.phosphorus}
                    onChange={(e) => handleInputChange("phosphorus", e.target.value)}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="potassium">Potassium (kg/ha)</Label>
                  <Input
                    id="potassium"
                    type="number"
                    placeholder="40"
                    value={formData.potassium}
                    onChange={(e) => handleInputChange("potassium", e.target.value)}
                  />
                </div>
              </div>

              <div className="flex space-x-2">
                <Button 
                  type="submit" 
                  className="flex-1 bg-agricultural-600 hover:bg-agricultural-700"
                  loading={isLoading}
                  disabled={isLoading}
                >
                  Get Recommendations
                </Button>
                <Button type="button" variant="outline" onClick={resetForm}>
                  Reset
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>

        {/* Results */}
        <div className="space-y-6">
          {showResults && recommendations.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <BarChart3 className="h-5 w-5" />
                  <span>Recommended Crops</span>
                </CardTitle>
                <CardDescription>
                  Based on your field conditions, here are the best crop options
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {recommendations.map((crop, index) => (
                  <div key={index} className="p-4 border rounded-lg space-y-3">
                    <div className="flex items-center justify-between">
                      <h3 className="font-semibold text-lg">{crop.name}</h3>
                      <div className="flex items-center space-x-2">
                        <span className={`text-sm px-2 py-1 rounded ${
                          crop.confidence >= 0.8 ? 'bg-green-100 text-green-800' :
                          crop.confidence >= 0.6 ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          {Math.round(crop.confidence * 100)}% match
                        </span>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div className="flex items-center space-x-2">
                        <TrendingUp className="h-4 w-4 text-green-600" />
                        <span>Expected: {crop.expected_yield} tons/ha</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <BarChart3 className="h-4 w-4 text-blue-600" />
                        <span>Price: ₹{crop.market_price}/quintal</span>
                      </div>
                    </div>

                    <div>
                      <h4 className="font-medium mb-2">Why this crop?</h4>
                      <ul className="text-sm text-muted-foreground space-y-1">
                        {crop.reasons.map((reason, i) => (
                          <li key={i} className="flex items-center space-x-2">
                            <div className="w-1.5 h-1.5 bg-agricultural-600 rounded-full"></div>
                            <span>{reason}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          )}

          {!showResults && (
            <Card>
              <CardContent className="p-8 text-center">
                <Sprout className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
                <h3 className="font-medium mb-2">Ready to Find Your Perfect Crop?</h3>
                <p className="text-muted-foreground">
                  Fill in your field information and get AI-powered crop recommendations
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}
