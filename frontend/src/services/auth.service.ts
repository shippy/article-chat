// TODO: Implement redirects to Cognito hosted UI / backend API actions

import axios from 'axios'
import { API_URL } from './api.service'

const AUTH_URL: String = 'https://auth.journalarticle.chat'

export default {
  // Check whether the user is logged in by checking the API is_authenticated endpoint
  async isLoggedIn(): Promise<{ is_authenticated: boolean; user: string | null }> {
    const response = await axios.get(`${API_URL}/auth/is_authenticated`, { withCredentials: true })
    if (response.status === 200) {
      return response.data
    } else {
      return { is_authenticated: false, user: null }
    }
  }
}
