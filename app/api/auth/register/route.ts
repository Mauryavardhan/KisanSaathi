import { NextRequest, NextResponse } from 'next/server'
import bcrypt from 'bcryptjs'
import { prisma } from '@/lib/prisma'
import { z } from 'zod'

const registerSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
  phone: z.string().optional(),
  location: z.string().optional(),
})

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    // Validate request body
    const validatedData = registerSchema.parse(body)
    
    // Check if user already exists
    const existingUser = await prisma.user.findUnique({
      where: { email: validatedData.email }
    })
    
    if (existingUser) {
      return NextResponse.json(
        { message: 'User with this email already exists' },
        { status: 400 }
      )
    }
    
    // Hash password
    const hashedPassword = await bcrypt.hash(validatedData.password, 12)
    
    // Create user
    const user = await prisma.user.create({
      data: {
        name: validatedData.name,
        email: validatedData.email,
        password: hashedPassword,
        phone: validatedData.phone,
        location: validatedData.location,
      }
    })
    
    // Remove password from response
    const { password: _, ...userWithoutPassword } = user
    
    return NextResponse.json({
      message: 'User created successfully',
      user: userWithoutPassword
    }, { status: 201 })
    
  } catch (error) {
    console.error('Registration error:', error)
    
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { message: 'Invalid input data', errors: error.errors },
        { status: 400 }
      )
    }
    
    return NextResponse.json(
      { message: 'Internal server error' },
      { status: 500 }
    )
  }
}
