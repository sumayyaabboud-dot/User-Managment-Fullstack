export const useApi = () => {
  const fetchApi = async (url: string, options: any = {}) => {
    const config = useRuntimeConfig()
    const baseUrl = config.public.apiBase || 'http://127.0.0.1:8000'

    // get token from localStorage  by using the allowed way in Nuxt
    let token = null
    if (typeof window !== 'undefined') {
      token = localStorage.getItem('access_token')
    }
         // setting Headers
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...options.headers,
    }

    // add to Authorization Header in case token exist
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    const response = await fetch(`${baseUrl}${url}`, {
      ...options,
      headers,
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || 'error request')
    }

    return data
  }

  return { fetchApi }
}