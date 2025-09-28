import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function main() {
  console.log('Seeding database...')

  // Create agent configurations
  const agentConfigs = [
    {
      name: 'crop_recommendation',
      displayName: 'Crop Recommendation',
      description: 'Provides personalized crop recommendations based on soil, climate, and market conditions',
      endpoint: '/crop-recommendation',
      enabled: true,
      icon: 'Sprout',
      category: 'recommendation',
      parameters: JSON.stringify({
        required: ['soil_type', 'location'],
        optional: ['ph_level', 'nitrogen', 'phosphorus', 'potassium', 'season', 'previous_crop']
      })
    },
    {
      name: 'disease_detection',
      displayName: 'Disease Detection',
      description: 'Analyzes crop images to identify diseases and provides treatment recommendations',
      endpoint: '/disease-detection',
      enabled: true,
      icon: 'Shield',
      category: 'detection',
      parameters: JSON.stringify({
        required: ['image_data'],
        optional: ['crop_type', 'symptoms_description']
      })
    },
    {
      name: 'weather_advisory',
      displayName: 'Weather Advisory',
      description: 'Provides weather forecasts and agricultural advisories',
      endpoint: '/weather',
      enabled: true,
      icon: 'Cloud',
      category: 'advisory',
      parameters: JSON.stringify({
        required: ['location'],
        optional: ['days']
      })
    },
    {
      name: 'market_prices',
      displayName: 'Market Prices',
      description: 'Provides real-time market prices and trends for agricultural commodities',
      endpoint: '/market-prices',
      enabled: true,
      icon: 'TrendingUp',
      category: 'market',
      parameters: JSON.stringify({
        required: ['crop_name', 'location'],
        optional: ['market_type']
      })
    },
    {
      name: 'fertilizer_recommendation',
      displayName: 'Fertilizer Guide',
      description: 'Recommends optimal fertilizer usage based on soil and crop requirements',
      endpoint: '/fertilizer-recommendation',
      enabled: true,
      icon: 'BarChart3',
      category: 'recommendation',
      parameters: JSON.stringify({
        required: ['crop_type', 'soil_type'],
        optional: ['growth_stage', 'target_yield']
      })
    },
    {
      name: 'pest_control',
      displayName: 'Pest Control',
      description: 'Identifies pests and provides integrated pest management solutions',
      endpoint: '/pest-control',
      enabled: true,
      icon: 'Bug',
      category: 'advisory',
      parameters: JSON.stringify({
        required: ['crop_type'],
        optional: ['pest_symptoms', 'severity']
      })
    },
    {
      name: 'irrigation_planning',
      displayName: 'Irrigation Planner',
      description: 'Optimizes water usage with smart irrigation scheduling',
      endpoint: '/irrigation-planning',
      enabled: true,
      icon: 'Droplets',
      category: 'planning',
      parameters: JSON.stringify({
        required: ['crop_type', 'soil_type', 'location'],
        optional: ['field_size', 'water_source']
      })
    },
    {
      name: 'government_schemes',
      displayName: 'Government Schemes',
      description: 'Information about agricultural subsidies and government policies',
      endpoint: '/government-schemes',
      enabled: true,
      icon: 'Banknote',
      category: 'information',
      parameters: JSON.stringify({
        required: ['location'],
        optional: ['farmer_category', 'crop_type']
      })
    }
  ]

  for (const config of agentConfigs) {
    await prisma.agentConfig.upsert({
      where: { name: config.name },
      update: config,
      create: config
    })
  }

  console.log('Agent configurations seeded successfully')

  // Create sample user (for testing)
  const sampleUser = await prisma.user.upsert({
    where: { email: 'farmer@example.com' },
    update: {},
    create: {
      name: 'Sample Farmer',
      email: 'farmer@example.com',
      location: 'Punjab, India',
      language: 'en',
      farmerType: 'smallholder'
    }
  })

  console.log('Sample user created:', sampleUser.email)

  // Create sample chat session
  const chatSession = await prisma.chatSession.create({
    data: {
      userId: sampleUser.id,
      title: 'Welcome to Kisan Saathi',
      messages: {
        create: [
          {
            role: 'assistant',
            content: 'Welcome to Kisan Saathi! I\'m your AI farming assistant. I can help you with crop recommendations, disease detection, weather updates, market prices, and much more. What farming question do you have today?',
            metadata: JSON.stringify({
              agent_used: 'greeting',
              confidence: 1.0
            })
          }
        ]
      }
    }
  })

  console.log('Sample chat session created')

  // Create sample queries
  const sampleQueries = [
    {
      userId: sampleUser.id,
      query: 'What crops are best for sandy soil in Punjab?',
      response: 'For sandy soil in Punjab, I recommend wheat, barley, and mustard. These crops are well-suited to sandy soil conditions and the climate of Punjab. Wheat is particularly profitable during the Rabi season.',
      agentType: 'crop_recommendation',
      language: 'en',
      inputType: 'text',
      confidence: 0.95,
      processingTime: 1200,
      satisfied: true
    },
    {
      userId: sampleUser.id,
      query: 'Current weather forecast for wheat farming',
      response: 'The weather forecast for the next 7 days shows favorable conditions for wheat farming with temperatures ranging from 15-25°C and minimal rainfall expected. This is ideal for wheat growth during the current stage.',
      agentType: 'weather_advisory',
      language: 'en',
      inputType: 'text',
      confidence: 0.88,
      processingTime: 800,
      satisfied: true
    }
  ]

  for (const query of sampleQueries) {
    await prisma.query.create({
      data: query
    })
  }

  console.log('Sample queries created')

  console.log('Database seeded successfully! 🌾')
}

main()
  .catch((e) => {
    console.error(e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })
