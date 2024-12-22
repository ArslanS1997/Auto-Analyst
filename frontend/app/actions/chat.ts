'use server'

import { ChatCompletionMessage } from 'openai-edge'

export async function chat(messages: ChatCompletionMessage[]) {
  const lastMessage = messages[messages.length - 1]
  
  const response = await fetch('http://localhost:5000/api/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      dataset: 'default', // You might want to update this based on the uploaded file
      goal: lastMessage.content,
    }),
  })

  if (!response.ok) {
    throw new Error('Failed to fetch from Flask backend')
  }

  const data = await response.json()
  return JSON.stringify(data)
}

