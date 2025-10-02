import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

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