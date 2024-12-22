'use client'

// Import necessary dependencies
import { useState, useEffect } from 'react'
import { useChat } from 'ai/react'
import { ContentRenderer } from './components/ContentRenderer'
import { parseResponse } from './utils/parseResponse'
import { chat } from './actions/chat'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import Image from 'next/image'

export default function ChatBot() {
  // Initialize chat functionality using the useChat hook
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    onFinish: async (message) => {
      const response = await chat(messages);
      return response;
    }
  })
  // State for managing file upload
  const [file, setFile] = useState<File | null>(null)
  // State for tracking progress and current stage
  const [progress, setProgress] = useState(0)
  const [currentStage, setCurrentStage] = useState('')

  // Handle file selection
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0])
    }
  }

  // Handle file upload to backend
  const handleFileUpload = async () => {
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://localhost:5000/api/upload', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('File upload failed')
      }

      const result = await response.json()
      console.log(result.message)
      // You might want to update the chat with a success message
    } catch (error) {
      console.error('Error uploading file:', error)
      // You might want to update the chat with an error message
    }
  }

  // Effect to update progress and stage from assistant messages
  useEffect(() => {
    if (messages.length > 0) {
      const lastMessage = messages[messages.length - 1]
      if (lastMessage.role === 'assistant') {
        try {
          const parsedContent = JSON.parse(lastMessage.content)
          if (parsedContent.progress) {
            setProgress(parsedContent.progress)
          }
          if (parsedContent.currentStage) {
            setCurrentStage(parsedContent.currentStage)
          }
        } catch (error) {
          console.error('Error parsing message content:', error)
        }
      }
    }
  }, [messages])

  return (
    // Main container with responsive layout
    <div className="flex flex-col h-screen max-w-3xl mx-auto p-4">
      {/* Header with logo and title */}
      <div className="flex items-center gap-2 mb-4">
        <Image 
          src="/images/Auto analysts icon small.png"
          alt="Auto-Analyst Logo"
          width={50}
          height={50}
        />
        <h1 className="text-2xl font-bold">Auto-Analyst</h1>
      </div>
      {/* Chat messages container */}
      <Card className="flex-1 mb-4 overflow-hidden">
        <CardContent className="h-full overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div key={message.id} className={`${message.role === 'user' ? 'text-right' : 'text-left'}`}>
              <div
                className={`inline-block p-2 rounded-lg ${
                  message.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-muted'
                }`}
              >
                {/* Render user messages as plain text and assistant messages using ContentRenderer */}
                {message.role === 'user' ? (
                  <p>{message.content}</p>
                ) : (
                  parseResponse(message.content).map((content, index) => (
                    <ContentRenderer key={index} content={content} />
                  ))
                )}
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
      {/* Progress indicator */}
      <div className="mb-4">
        <Progress value={progress} className="w-full" />
        <p className="text-sm text-muted-foreground mt-2">{currentStage}</p>
      </div>
      {/* File upload section */}
      <div className="flex space-x-2 mb-4">
        <Input type="file" onChange={handleFileChange} accept=".csv" />
        <Button onClick={handleFileUpload} disabled={!file}>Upload</Button>
      </div>
      {/* Chat input form */}
      <form onSubmit={handleSubmit} className="flex space-x-2">
        <Input
          type="text"
          value={input}
          onChange={handleInputChange}
          placeholder="Type your message..."
          className="flex-1"
        />
        <Button type="submit">Send</Button>
      </form>
    </div>
  )
}
