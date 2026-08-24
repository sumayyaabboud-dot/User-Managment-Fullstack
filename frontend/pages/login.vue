<template>
  <div class="min-h-screen grid grid-cols-1 lg:grid-cols-2 bg-[#0B0F17]">
    
    <!-- Left Section -->
    <div class="hidden lg:flex flex-col justify-between p-12 bg-gradient-to-br from-indigo-950/40 via-slate-900 to-[#0B0F17] border-r border-slate-800/60 relative overflow-hidden">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/30">
          U
        </div>
        <span class="text-xl font-semibold tracking-wide text-white">UserHub<span class="text-indigo-400">.Pro</span></span>
      </div>

      <div class="space-y-4 max-w-md">
        <h1 class="text-4xl font-bold text-white leading-tight">Welcome Back</h1>
        <p class="text-slate-400 text-sm leading-relaxed">Sign in to manage your account and access your dashboard.</p>
      </div>

      <div class="text-xs text-slate-500">&copy; 2026 UserHub. All rights reserved.</div>
    </div>

    <!-- Right Section: Login Form -->
    <div class="flex items-center justify-center p-8 sm:p-12">
      <div class="w-full max-w-md space-y-6 bg-slate-900/50 p-8 rounded-2xl border border-slate-800/80 backdrop-blur-xl shadow-2xl">
        
        <div>
          <h2 class="text-2xl font-bold text-white tracking-tight">Login</h2>
          <p class="text-slate-400 text-sm mt-1">Enter your credentials to access your account</p>
        </div>

        <div v-if="errorMessage" class="p-3.5 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-xs">
          {{ errorMessage }}
        </div>

        <form @submit.prevent="handleLogin" class="space-y-4" autocomplete="off">
          <div>
            <label class="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-2">Email Address</label>
          <input 
            v-model="form.email" 
            type="email" 
              name="email" 
              autocomplete="off" 
            required
              placeholder="admin@example.com" 
              class="w-full px-4 py-3 bg-slate-950/60 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-600 text-sm focus:outline-none focus:border-indigo-500 transition-all" 
          />
        </div>

        <div>
            <label class="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-2">Password</label>
          <input 
            v-model="form.password" 
            type="password" 
              name="password" 
              autocomplete="new-password" 
            required
            placeholder="••••••••"
              class="w-full px-4 py-3 bg-slate-950/60 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-600 text-sm focus:outline-none focus:border-indigo-500 transition-all" 
          />
        </div>

          <button type="submit" :disabled="loading" class="w-full py-3.5 px-4 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-xl text-sm transition-all shadow-lg shadow-indigo-600/25 flex items-center justify-center gap-2 disabled:opacity-50">
            <span>{{ loading ? 'Signing in...' : 'Sign In' }}</span>
        </button>
      </form>

        <p class="text-center text-xs text-slate-400">
          Don't have an account? 
          <NuxtLink to="/register" class="text-indigo-400 hover:text-indigo-300 font-medium transition-colors">Sign up</NuxtLink>
        </p>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useApi } from '~/composables/useApi'

const { fetchApi } = useApi()
const loading = ref(false)
const errorMessage = ref('')

const form = reactive({
  email: '',
  password: ''
})

const handleLogin = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const response = await fetchApi('/auth/login', {
      method: 'POST',
      body: JSON.stringify(form)
    })

    if (response && response.access_token) {
      if (typeof window !== 'undefined') {
        localStorage.setItem('access_token', response.access_token)
    }
    navigateTo('/')
    }
  } catch (error) {
    errorMessage.value = error.message || 'Invalid email or password'
  } finally {
    loading.value = false
  }
}
</script>