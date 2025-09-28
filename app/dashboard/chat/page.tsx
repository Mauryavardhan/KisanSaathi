"use client"

import { useState, useRef, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { 
  Send, 
  Mic, 
  MicOff, 
  Image, 
  Loader2, 
  Bot, 
  User, 
  Volume2,
  Copy,
  ThumbsUp,
  ThumbsDown
} from "lucide-react"
import { useSession } from "next-auth/react"
import { api } from "@/lib/api"
import toast from "react-hot-toast"
import { cn, getInitials } from "@/lib/utils"

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  metadata?: {
    agent_used?: string
    confidence?: number
    processing_time?: number
  }
}

const sampleQuestions = [
  "What's the best crop for this season?",
  "How to treat tomato blight disease?",
  "When should I irrigate my wheat field?",
  "Current market price of rice?",
  "Best fertilizer for cotton crop?",
  "How to control pest in my vegetable garden?"
]

export default function ChatPage() {
  const { data: session } = useSession()
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your AI farming assistant. I can help you with crop recommendations, disease detection, weather updates, market prices, and much more. What farming question do you have today?',
      timestamp: new Date(),
      metadata: {
        agent_used: 'greeting',
        confidence: 1.0
      }
    }
  ])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isListening, setIsListening] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async (messageText?: string) => {
    const text = messageText || inputValue.trim()
    if (!text) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      const response = await api.query({
        query: text,
        language: 'en',
        input_type: 'text'
      })

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
        metadata: {
          agent_used: response.agent_used,
          confidence: response.confidence,
          processing_time: response.processing_time
        }
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Chat error:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'I apologize, but I\'m having trouble connecting to my agricultural knowledge base right now. Please try again in a moment, or feel free to ask your question in a different way.',
        timestamp: new Date(),
        metadata: {
          agent_used: 'error_handler',
          confidence: 0.0
        }
      }
      setMessages(prev => [...prev, errorMessage])
      toast.error('Failed to get response. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const handleVoiceInput = async () => {
    if (!isListening) {
      // Start voice recording
      setIsListening(true)
      toast.success('Voice recording started...')
      // Voice recording implementation would go here
      // For now, just simulate it
      setTimeout(() => {
        setIsListening(false)
        toast.success('Voice recording stopped')
      }, 3000)
    } else {
      // Stop voice recording
      setIsListening(false)
      toast.success('Voice recording stopped')
    }
  }

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      // Handle image upload for disease detection
      const reader = new FileReader()
      reader.onload = (e) => {
        const imageData = e.target?.result as string
        handleSendMessage(`[Image uploaded: ${file.name}] Can you analyze this crop image for any diseases or issues?`)
      }
      reader.readAsDataURL(file)
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    toast.success('Copied to clipboard!')
  }

  const formatTimestamp = (timestamp: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    }).format(timestamp)
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'text-green-600'
    if (confidence >= 0.6) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <div className="h-full flex flex-col p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold">AI Chat Assistant</h1>
        <p className="text-muted-foreground">
          Ask me anything about farming, crops, diseases, weather, and more!
        </p>
      </div>

      <div className="flex-1 flex gap-6">
        {/* Chat Area */}
        <div className="flex-1 flex flex-col">
          <Card className="flex-1 flex flex-col">
            {/* Messages */}
            <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={cn(
                    "flex items-start space-x-3",
                    message.role === 'user' ? 'justify-end' : 'justify-start'
                  )}
                >
                  {message.role === 'assistant' && (
                    <Avatar className="h-8 w-8 bg-agricultural-100">
                      <AvatarFallback>
                        <Bot className="h-4 w-4 text-agricultural-600" />
                      </AvatarFallback>
                    </Avatar>
                  )}
                  
                  <div className={cn(
                    "max-w-[80%] space-y-2",
                    message.role === 'user' ? 'order-first' : ''
                  )}>
                    <div className={cn(
                      "p-3 rounded-lg",
                      message.role === 'user' 
                        ? 'bg-agricultural-600 text-white ml-auto' 
                        : 'bg-muted'
                    )}>
                      <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                    </div>
                    
                    <div className={cn(
                      "flex items-center space-x-2 text-xs text-muted-foreground",
                      message.role === 'user' ? 'justify-end' : 'justify-start'
                    )}>
                      <span>{formatTimestamp(message.timestamp)}</span>
                      
                      {message.role === 'assistant' && message.metadata && (
                        <>
                          {message.metadata.agent_used && (
                            <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded">
                              {message.metadata.agent_used}
                            </span>
                          )}
                          {message.metadata.confidence && (
                            <span className={cn(
                              "px-2 py-1 rounded",
                              getConfidenceColor(message.metadata.confidence)
                            )}>
                              {Math.round(message.metadata.confidence * 100)}% confident
                            </span>
                          )}
                        </>
                      )}
                      
                      {message.role === 'assistant' && (
                        <div className="flex items-center space-x-1">
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-6 w-6 p-0"
                            onClick={() => copyToClipboard(message.content)}
                          >
                            <Copy className="h-3 w-3" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-6 w-6 p-0"
                          >
                            <Volume2 className="h-3 w-3" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-6 w-6 p-0"
                          >
                            <ThumbsUp className="h-3 w-3" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-6 w-6 p-0"
                          >
                            <ThumbsDown className="h-3 w-3" />
                          </Button>
                        </div>
                      )}
                    </div>
                  </div>

                  {message.role === 'user' && (
                    <Avatar className="h-8 w-8">
                      <AvatarImage src={session?.user?.image || ""} />
                      <AvatarFallback className="bg-agricultural-100 text-agricultural-800">
                        {getInitials(session?.user?.name || 'U')}
                      </AvatarFallback>
                    </Avatar>
                  )}
                </div>
              ))}
              
              {isLoading && (
                <div className="flex items-start space-x-3">
                  <Avatar className="h-8 w-8 bg-agricultural-100">
                    <AvatarFallback>
                      <Bot className="h-4 w-4 text-agricultural-600" />
                    </AvatarFallback>
                  </Avatar>
                  <div className="bg-muted p-3 rounded-lg">
                    <div className="flex items-center space-x-2">
                      <Loader2 className="h-4 w-4 animate-spin" />
                      <span className="text-sm">Thinking...</span>
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </CardContent>

            {/* Input Area */}
            <div className="border-t p-4">
              <div className="flex items-center space-x-2">
                <Button
                  variant="outline"
                  size="icon"
                  onClick={() => fileInputRef.current?.click()}
                  className="shrink-0"
                >
                  <Image className="h-4 w-4" />
                </Button>
                
                <Button
                  variant="outline"
                  size="icon"
                  onClick={handleVoiceInput}
                  className={cn(
                    "shrink-0",
                    isListening && "bg-red-100 text-red-600"
                  )}
                >
                  {isListening ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
                </Button>

                <Input
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask about farming, crops, diseases, weather..."
                  className="flex-1"
                  disabled={isLoading}
                />

                <Button
                  onClick={() => handleSendMessage()}
                  disabled={isLoading || !inputValue.trim()}
                  className="shrink-0"
                >
                  <Send className="h-4 w-4" />
                </Button>

                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleImageUpload}
                  className="hidden"
                />
              </div>
            </div>
          </Card>
        </div>

        {/* Sidebar with suggestions */}
        <div className="w-80 space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Quick Questions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {sampleQuestions.map((question, index) => (
                <Button
                  key={index}
                  variant="outline"
                  size="sm"
                  className="w-full justify-start text-left h-auto p-3 whitespace-normal"
                  onClick={() => handleSendMessage(question)}
                  disabled={isLoading}
                >
                  {question}
                </Button>
              ))}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Features</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="text-sm space-y-2">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span>Multilingual support</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span>Voice input/output</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span>Image analysis</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span>Real-time data</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span>Expert recommendations</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
