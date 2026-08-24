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
        <h1 class="text-4xl font-bold text-white leading-tight">Create an Account</h1>
        <p class="text-slate-400 text-sm leading-relaxed">Join the platform to access your dashboard and manage permissions.</p>
      </div>

      <div class="text-xs text-slate-500">&copy; 2026 UserHub. All rights reserved.</div>
    </div>

    <!-- Right Section: Register Form -->
    <div class="flex items-center justify-center p-8 sm:p-12">
      <div class="w-full max-w-md space-y-6 bg-slate-900/50 p-8 rounded-2xl border border-slate-800/80 backdrop-blur-xl shadow-2xl">
        
        <div>
          <h2 class="text-2xl font-bold text-white tracking-tight">Register</h2>
          <p class="text-slate-400 text-sm mt-1">Enter your details to create an account</p>
        </div>

        <div v-if="errorMessage" class="p-3.5 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-xs">
          {{ errorMessage }}
        </div>

        <div v-if="successMessage" class="p-3.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs">
          {{ successMessage }}
        </div>

        <form @submit.prevent="handleRegister" class="space-y-4">
        <div class="grid grid-cols-2 gap-3">
          <div>
              <label class="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-2">First Name</label>
              <input v-model="form.first_name" type="text" required placeholder="John" class="w-full px-4 py-3 bg-slate-950/60 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-600 text-sm focus:outline-none focus:border-indigo-500 transition-all" />
            </div>
            <div>
              <label class="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-2">Last Name</label>
              <input v-model="form.last_name" type="text" required placeholder="Doe" class="w-full px-4 py-3 bg-slate-950/60 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-600 text-sm focus:outline-none focus:border-indigo-500 transition-all" />
            </div>
          </div>

          <div>
            <label class="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-2">Email Address</label>
            <input v-model="form.email" type="email" required placeholder="user@example.com" class="w-full px-4 py-3 bg-slate-950/60 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-600 text-sm focus:outline-none focus:border-indigo-500 transition-all" />
        </div>

          <div class="grid grid-cols-2 gap-3">
        <div>
              <label class="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-2">Phone</label>
              <input v-model="form.phone" type="text" required placeholder="+96170123456" class="w-full px-4 py-3 bg-slate-950/60 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-600 text-sm focus:outline-none focus:border-indigo-500 transition-all" />
            </div>
            <div>
              <label class="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-2">City</label>
              <input v-model="form.city" type="text" required placeholder="Beirut" class="w-full px-4 py-3 bg-slate-950/60 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-600 text-sm focus:outline-none focus:border-indigo-500 transition-all" />
            </div>
          </div>

          <div>
            <label class="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-2">Age</label>
            <input v-model.number="form.age" type="number" min="1" max="119" required placeholder="25" class="w-full px-4 py-3 bg-slate-950/60 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-600 text-sm focus:outline-none focus:border-indigo-500 transition-all" />
        </div>



        <div>
            <label class="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-2">Password (Min 8 chars)</label>
            <input v-model="form.password" type="password" minlength="8" required placeholder="••••••••" class="w-full px-4 py-3 bg-slate-950/60 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-600 text-sm focus:outline-none focus:border-indigo-500 transition-all" />
        </div>

          <button type="submit" :disabled="loading" class="w-full py-3.5 px-4 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-xl text-sm transition-all shadow-lg shadow-indigo-600/25 flex items-center justify-center gap-2 disabled:opacity-50">
            <span>{{ loading ? 'Creating Account...' : 'Sign Up' }}</span>
        </button>
      </form>

        <p class="text-center text-xs text-slate-400">
          Already have an account? 
          <NuxtLink to="/login" class="text-indigo-400 hover:text-indigo-300 font-medium transition-colors">Sign in</NuxtLink>
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
const successMessage = ref('')

const form = reactive({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  city: '',
  age: null,
  password: '',
  
})

const handleRegister = async () => {
  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await fetchApi('/auth/register', {
      method: 'POST',
      body: JSON.stringify(form)
    })
    successMessage.value = 'Account created successfully! Redirecting to login...'
    setTimeout(() => {
    navigateTo('/login')
    }, 1500)
  } catch (error) {
    errorMessage.value = error.message || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>