import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET() {
  try {
    // Check database connection
    await prisma.$queryRaw`SELECT 1`
    
    // Check backend API connection
    const backendHealth = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/health`, {
      method: 'GET',
      timeout: 5000
    }).then(res => res.ok).catch(() => false)

    const healthData = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      database: 'connected',
      backend: backendHealth ? 'connected' : 'disconnected',
      version: process.env.npm_package_version || '1.0.0',
      environment: process.env.NODE_ENV
    }

    return NextResponse.json(healthData)
  } catch (error) {
    const errorData = {
      status: 'unhealthy',
      timestamp: new Date().toISOString(),
      error: error instanceof Error ? error.message : 'Unknown error',
      database: 'disconnected',
      environment: process.env.NODE_ENV
    }

    return NextResponse.json(errorData, { status: 503 })
  }
}
