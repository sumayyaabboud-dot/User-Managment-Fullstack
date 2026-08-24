import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: typeof window !== 'undefined' ? localStorage.getItem('access_token') || null : null,
    user: null as any
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => (state.user?.type || state.user?.role) === 'admin'
  },
  actions: {
    setToken(token: string) {
      this.token = token
      if (typeof window !== 'undefined') {
        localStorage.setItem('access_token', token)
      }
    },
    setUser(userData: any) {
      this.user = userData
    },
    logout() {
      this.token = null
      this.user = null
      if (typeof window !== 'undefined') {
        localStorage.removeItem('access_token')
      }
      navigateTo('/login')
    }
  }
})