export type ContentType = 'text' | 'code' | 'markdown' | 'chart' | 'plan' | 'agent_output' | 'json'

export interface ParsedContent {
  type: ContentType
  content: string
  agentName?: string
}

export function parseResponse(response: string): ParsedContent[] {
  try {
    const parsedResponse = JSON.parse(response)
    const result: ParsedContent[] = []

    if (parsedResponse.analytical_planner) {
      result.push({ type: 'plan', content: parsedResponse.analytical_planner.plan })
      result.push({ type: 'text', content: parsedResponse.analytical_planner.plan_desc })
    }

    for (const key in parsedResponse) {
      if (key !== 'analytical_planner' && key !== 'code_combiner_agent' && key !== 'memory_combined') {
        const agentOutput = parsedResponse[key]
        if (agentOutput.code) {
          result.push({ type: 'code', content: agentOutput.code })
        }
        if (agentOutput.commentary) {
          result.push({ type: 'agent_output', content: agentOutput.commentary, agentName: key })
        }
      }
    }

    if (parsedResponse.code_combiner_agent) {
      result.push({ type: 'code', content: parsedResponse.code_combiner_agent.refined_complete_code })
    }

    if (parsedResponse.memory_combined) {
      result.push({ type: 'text', content: parsedResponse.memory_combined })
    }

    return result
  } catch (error) {
    // If parsing fails, treat it as plain text
    return [{ type: 'text', content: response }]
  }
}

