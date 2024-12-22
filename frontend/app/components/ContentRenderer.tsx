'use client'

import { useState, useEffect } from 'react'
import dynamic from 'next/dynamic'
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter'
import { docco } from 'react-syntax-highlighter/dist/esm/styles/hljs'
import ReactMarkdown from 'react-markdown'
import { ParsedContent } from '../utils/parseResponse'

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false })

export function ContentRenderer({ content }: { content: ParsedContent }) {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  switch (content.type) {
    case 'text':
      return <p className="mb-2">{content.content}</p>
    case 'code':
      return (
        <div className="mb-4">
          <SyntaxHighlighter language="python" style={docco}>
            {content.content}
          </SyntaxHighlighter>
        </div>
      )
    case 'markdown':
      return <ReactMarkdown className="mb-4">{content.content}</ReactMarkdown>
    case 'chart':
      if (!mounted) return null
      try {
        const chartData = JSON.parse(content.content)
        return (
          <div className="mb-4">
            <Plot data={chartData.data} layout={chartData.layout} />
          </div>
        )
      } catch (error) {
        return <p className="text-red-500 mb-2">Error rendering chart: {(error as Error).message}</p>
      }
    case 'plan':
      return (
        <div className="mb-4">
          <h3 className="font-bold">Plan:</h3>
          <p>{content.content}</p>
        </div>
      )
    case 'agent_output':
      return (
        <div className="mb-4">
          <h3 className="font-bold">{content.agentName} Output:</h3>
          <p>{content.content}</p>
        </div>
      )
    default:
      return <p className="mb-2">{JSON.stringify(content)}</p>
  }
}

