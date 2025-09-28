// User types
export interface User {
  id: string
  name?: string
  email: string
  image?: string
  phone?: string
  location?: string
  language: string
  farmerType?: string
  createdAt: Date
  updatedAt: Date
}

// Chat types
export interface ChatSession {
  id: string
  userId: string
  title?: string
  createdAt: Date
  updatedAt: Date
  messages: Message[]
}

export interface Message {
  id: string
  chatSessionId: string
  role: 'user' | 'assistant' | 'system'
  content: string
  metadata?: Record<string, any>
  createdAt: Date
}

// Query types
export interface Query {
  id: string
  userId: string
  query: string
  response?: string
  agentType?: string
  language: string
  inputType: 'text' | 'voice' | 'image'
  confidence?: number
  processingTime?: number
  satisfied?: boolean
  createdAt: Date
}

// Agent types
export interface AgentConfig {
  id: string
  name: string
  displayName: string
  description: string
  endpoint: string
  enabled: boolean
  icon?: string
  category: string
  parameters?: Record<string, any>
}

export interface AgentResponse {
  response: string
  confidence: number
  metadata?: Record<string, any>
  suggestions?: string[]
}

// Agricultural domain types
export interface CropInfo {
  name: string
  scientificName?: string
  category: string
  season: 'kharif' | 'rabi' | 'zaid'
  growthPeriod: number // days
  expectedYield: number // tons per hectare
  waterRequirement: 'low' | 'medium' | 'high'
  soilType: string[]
  description?: string
}

export interface SoilData {
  ph: number
  nitrogen: number
  phosphorus: number
  potassium: number
  organicMatter: number
  moisture: number
  soilType: string
  location: string
}

export interface WeatherData {
  temperature: number
  humidity: number
  rainfall: number
  windSpeed: number
  weatherCondition: string
  forecast: WeatherForecast[]
}

export interface WeatherForecast {
  date: string
  temperatureMin: number
  temperatureMax: number
  rainfallProbability: number
  weatherCondition: string
}

export interface Disease {
  name: string
  scientificName?: string
  symptoms: string[]
  causes: string[]
  treatmentOptions: TreatmentOption[]
  preventionMeasures: string[]
  severity: 'low' | 'medium' | 'high' | 'critical'
  affectedCrops: string[]
  seasonality?: string[]
}

export interface TreatmentOption {
  type: 'organic' | 'chemical' | 'biological'
  name: string
  description: string
  applicationMethod: string
  dosage?: string
  frequency?: string
  cost?: number
  effectiveness: number // 0-100
}

export interface Pest {
  name: string
  scientificName?: string
  description: string
  identification: string[]
  damageSymptoms: string[]
  controlMeasures: ControlMeasure[]
  affectedCrops: string[]
  lifecycle?: string
  seasonality?: string[]
}

export interface ControlMeasure {
  type: 'cultural' | 'biological' | 'chemical' | 'integrated'
  name: string
  description: string
  effectiveness: number
  cost?: number
  environmentalImpact: 'low' | 'medium' | 'high'
}

export interface FertilizerRecommendation {
  type: 'organic' | 'inorganic' | 'bio'
  name: string
  composition: {
    nitrogen: number
    phosphorus: number
    potassium: number
  }
  applicationRate: string
  applicationTiming: string[]
  benefits: string[]
  precautions?: string[]
  cost?: number
}

export interface MarketPrice {
  cropName: string
  location: string
  marketType: 'wholesale' | 'retail' | 'mandi'
  currentPrice: number
  priceUnit: string
  priceDate: Date
  trend: 'increasing' | 'decreasing' | 'stable'
  priceHistory: PriceHistory[]
}

export interface PriceHistory {
  date: Date
  price: number
  volume?: number
}

export interface GovernmentScheme {
  id: string
  name: string
  description: string
  eligibility: string[]
  benefits: string[]
  applicationProcess: string[]
  documents: string[]
  lastDate?: Date
  contactInfo: ContactInfo
  category: 'subsidy' | 'loan' | 'insurance' | 'training' | 'equipment'
}

export interface ContactInfo {
  department: string
  phone?: string
  email?: string
  website?: string
  address?: string
}

// UI Component types
export interface SelectOption {
  value: string
  label: string
  description?: string
  icon?: string
}

export interface FormField {
  name: string
  label: string
  type: 'text' | 'email' | 'password' | 'number' | 'select' | 'textarea' | 'file'
  placeholder?: string
  required?: boolean
  options?: SelectOption[]
  validation?: {
    min?: number
    max?: number
    pattern?: string
    message?: string
  }
}

export interface UploadedFile {
  file: File
  preview?: string
  progress?: number
  error?: string
}

// API Response types
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  message?: string
  error?: string
  code?: string
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  limit: number
  totalPages: number
  hasNext: boolean
  hasPrev: boolean
}

// Language and localization
export interface Language {
  code: string
  name: string
  nativeName: string
  flag?: string
  supported: boolean
}

export interface LocaleString {
  [locale: string]: string
}

// Notification types
export interface Notification {
  id: string
  type: 'info' | 'success' | 'warning' | 'error'
  title: string
  message: string
  timestamp: Date
  read: boolean
  actionUrl?: string
  actionText?: string
}

// Dashboard types
export interface DashboardStats {
  totalQueries: number
  resolvedQueries: number
  averageResponseTime: number
  userSatisfaction: number
  popularAgents: AgentUsage[]
  recentActivity: Activity[]
}

export interface AgentUsage {
  agent: string
  count: number
  percentage: number
}

export interface Activity {
  id: string
  type: 'query' | 'recommendation' | 'detection'
  description: string
  timestamp: Date
  status: 'success' | 'pending' | 'failed'
}

// Feature configuration
export interface FeatureConfig {
  name: string
  displayName: string
  description: string
  icon: string
  enabled: boolean
  category: string
  route: string
  requiresAuth: boolean
  beta?: boolean
}

export type Theme = 'light' | 'dark' | 'system'

export type ViewMode = 'grid' | 'list' | 'card'

export type SortOrder = 'asc' | 'desc'

export interface SearchFilters {
  query?: string
  category?: string
  dateRange?: {
    from: Date
    to: Date
  }
  location?: string
  language?: string
}
