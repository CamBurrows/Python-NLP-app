import axios from 'axios'

// Use environment variable for API URL, fallback to localhost for development
const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:5000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // Increased timeout for Lambda cold starts
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor for debugging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`Making request to: ${config.baseURL}${config.url}`)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK') {
      console.error('Network error: Unable to connect to API server')
    }
    return Promise.reject(error)
  }
)

export const nlpService = {
  /**
   * Analyze a word using the NLP API
   * @param {string} word - The word to analyze
   * @returns {Promise} API response with word analysis
   */
  async analyzeWord(word) {
    try {
      const response = await apiClient.post('/analyze', { word })
      return response.data
    } catch (error) {
      if (error.response && error.response.data) {
        throw new Error(error.response.data.error || 'Analysis failed')
      }
      throw new Error('Network error: Unable to connect to the server')
    }
  },

  /**
   * Check API health status
   * @returns {Promise} API health status
   */
  async checkHealth() {
    try {
      const response = await apiClient.get('/health')
      return response.data
    } catch (error) {
      throw new Error('Unable to connect to the server')
    }
  },
}