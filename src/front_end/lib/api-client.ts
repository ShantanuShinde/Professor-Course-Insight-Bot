// This is a simple API client that you can use to connect to your Python backend

export interface ChatResponse {
    response: string
    error?: string
  }
  
  export class ApiClient {
    private baseUrl: string
  
    constructor(baseUrl = "/api") {
      this.baseUrl = baseUrl
    }
  
    async sendMessage(message: string): Promise<ChatResponse> {
      try {
        const response = await fetch(`${this.baseUrl}/chat`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message }),
        })
  
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
  
        return await response.json()
      } catch (error) {
        console.error("Error sending message:", error)
        return {
          response: "Sorry, there was an error processing your request.",
          error: error instanceof Error ? error.message : "Unknown error",
        }
      }
    }
  }
  
  // Create a singleton instance with the default base URL
  export const apiClient = new ApiClient()
  