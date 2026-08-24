<template>
  <div class="min-h-screen bg-[#0B0F17] text-slate-100 flex flex-col">
    <!-- Header / Navbar -->
    <header class="border-b border-slate-800 bg-slate-900/50 backdrop-blur-xl px-6 py-4 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-indigo-600 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/30">
          U
        </div>
        <span class="text-lg font-semibold tracking-wide text-white">UserHub<span class="text-indigo-400">.Pro</span></span>
      </div>

      <div class="flex items-center gap-4" v-if="user">

  <button 
    v-if="(user.type || user.role) === 'admin'"
    @click="showCreateAdminModal = true" 
    class="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white text-xs rounded-lg font-medium transition-colors"
  >
    + Add Admin
  </button>

  <span class="text-xs px-2.5 py-1 rounded-full font-medium uppercase"
        :class="(user.type || user.role) === 'admin' ? 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20' : 'bg-slate-800 text-slate-400'">
    {{ user.type || user.role }}
  </span>

  <button @click="handleLogout" class="px-4 py-2 bg-red-500/10 hover:bg-red-500/20 text-red-400 text-xs rounded-lg transition-colors">
    Logout
  </button>
</div>
    </header>

    <!-- Main Content Area -->
    <main class="flex-1 p-6 md:p-12 max-w-6xl mx-auto w-full space-y-8">
      <div v-if="loading" class="text-center py-20 text-slate-500 text-sm">
        Loading dashboard data...
      </div>

      <template v-else-if="user">
        <!-- Welcome Card -->
        <div class="bg-slate-900/40 border border-slate-800 p-8 rounded-2xl backdrop-blur-xl shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div class="space-y-1">
            <h1 class="text-2xl font-bold text-white">Welcome back, {{ user.first_name }} {{ user.last_name }}! 👋</h1>
            <p class="text-sm text-slate-400">You are successfully authenticated and logged into your dashboard.</p>
          </div>
          <button @click="openEditModal" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium rounded-xl shadow-lg shadow-indigo-600/20 transition-all self-start md:self-auto">
            Edit Profile
          </button>
        </div>

        <!-- User Profile Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-slate-900/30 border border-slate-800/80 p-5 rounded-xl space-y-1">
            <span class="text-xs text-slate-500 uppercase font-medium">Email</span>
            <p class="text-sm font-semibold text-slate-200">{{ user.email }}</p>
          </div>

          <div class="bg-slate-900/30 border border-slate-800/80 p-5 rounded-xl space-y-1">
            <span class="text-xs text-slate-500 uppercase font-medium">Phone</span>
            <p class="text-sm font-semibold text-slate-200">{{ user.phone }}</p>
          </div>

          <div class="bg-slate-900/30 border border-slate-800/80 p-5 rounded-xl space-y-1">
            <span class="text-xs text-slate-500 uppercase font-medium">City & Age</span>
            <p class="text-sm font-semibold text-slate-200">{{ user.city }} ({{ user.age }} yo)</p>
          </div>
        </div>

        <!-- ADMIN ONLY SECTION: System Analytics -->
        <div v-if="(user.type || user.role) === 'admin'" class="space-y-4 pt-2">
          <h2 class="text-lg font-bold text-white">System Analytics</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="bg-indigo-950/20 border border-indigo-500/20 p-5 rounded-xl space-y-1">
              <span class="text-xs text-indigo-400 uppercase font-medium">Total Users</span>
              <p class="text-2xl font-bold text-white">{{ stats.userCount !== null ? stats.userCount : '-' }}</p>
            </div>

            <div class="bg-indigo-950/20 border border-indigo-500/20 p-5 rounded-xl space-y-1">
              <span class="text-xs text-indigo-400 uppercase font-medium">Average Age</span>
              <p class="text-2xl font-bold text-white">{{ stats.averageAge !== null ? stats.averageAge : '-' }} <span class="text-xs font-normal text-slate-400">years</span></p>
            </div>

            <div class="bg-indigo-950/20 border border-indigo-500/20 p-5 rounded-xl space-y-1">
              <span class="text-xs text-indigo-400 uppercase font-medium">Top Cities</span>
              <p class="text-sm font-semibold text-slate-200 truncate">{{ stats.topCities || '-' }}</p>
            </div>
          </div>
        </div>

        <!-- ADMIN ONLY SECTION: Users Management Table -->
        <div v-if="(user.type || user.role) === 'admin'" class="space-y-4 pt-4">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-xl font-bold text-white">User Management</h2>
              <p class="text-xs text-slate-400">View and manage all registered users in the system</p>
            </div>
            <button @click="loadUsersList" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs rounded-lg border border-slate-700 transition-all">
              Refresh List
            </button>
          </div>

          <!-- Search & Filter Controls -->
          <div class="flex flex-col sm:flex-row gap-3 justify-between items-center bg-slate-900/40 border border-slate-800 p-3.5 rounded-xl backdrop-blur-xl">
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Search by name or email..." 
              class="w-full sm:w-80 px-3.5 py-1.5 bg-slate-950 border border-slate-800 rounded-lg text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-all"
            />
            <div class="flex items-center gap-2 w-full sm:w-auto justify-end">
              <span class="text-xs text-slate-400 font-medium">Role:</span>
              <select 
                v-model="filterType" 
                class="px-3 py-1.5 bg-slate-950 border border-slate-800 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-indigo-500 transition-all"
              >
                <option value="all">All Roles</option>
                <option value="admin">Admin</option>
                <option value="client">Client</option>
              </select>
            </div>
          </div>

          <!-- Users Table -->
          <div class="bg-slate-900/40 border border-slate-800 rounded-2xl overflow-hidden backdrop-blur-xl shadow-xl">
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="border-b border-slate-800 bg-slate-950/40 text-xs uppercase text-slate-400 font-semibold tracking-wider">
                    <th class="p-4">Name</th>
                    <th class="p-4">Email</th>
                    <th class="p-4">Type</th>
                    <th class="p-4">City</th>
                    <th class="p-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-800/60 text-sm">
                  <tr v-if="filteredUsersList.length === 0">
                    <td colspan="5" class="p-8 text-center text-slate-500 text-xs">No matching users found.</td>
                  </tr>
                  <tr v-for="item in filteredUsersList" :key="item.id || item._id" class="hover:bg-slate-800/20 transition-colors">
                    <td class="p-4 font-medium text-slate-200">{{ item.first_name }} {{ item.last_name }}</td>
                    <td class="p-4 text-slate-400">{{ item.email }}</td>
                    <td class="p-4">
                      <span class="text-xs px-2 py-0.5 rounded-full font-medium"
                            :class="(item.type || item.role) === 'admin' ? 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20' : 'bg-slate-800 text-slate-300'">
                        {{ item.type || item.role }}
                      </span>
                    </td>
                    <td class="p-4 text-slate-400">{{ item.city || '-' }}</td>
                    <td class="p-4 text-right">
                      <button 
                        @click="handleDeleteUser(item.id || item._id)" 
                        :disabled="(item.id || item._id) === (user.id || user._id)"
                        class="px-3 py-1 bg-red-500/10 hover:bg-red-500/20 text-red-400 text-xs font-medium rounded-lg border border-red-500/20 transition-all disabled:opacity-30 disabled:cursor-not-allowed">
                        Delete
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>



      </template>
    </main>

    <!-- Edit Profile Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl w-full max-w-md space-y-4 shadow-2xl">
        <h3 class="text-lg font-bold text-white">Edit Profile</h3>

        <form @submit.prevent="handleUpdateProfile" class="space-y-3">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-medium text-slate-400 mb-1">First Name</label>
              <input v-model="editForm.first_name" type="text" class="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-indigo-500" required />
            </div>
            <div>
              <label class="block text-xs font-medium text-slate-400 mb-1">Last Name</label>
              <input v-model="editForm.last_name" type="text" class="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-indigo-500" required />
            </div>
          </div>

          <div>
            <label class="block text-xs font-medium text-slate-400 mb-1">Phone</label>
            <input v-model="editForm.phone" type="text" class="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-indigo-500" required />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-medium text-slate-400 mb-1">City</label>
              <input v-model="editForm.city" type="text" class="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-indigo-500" required />
            </div>
            <div>
              <label class="block text-xs font-medium text-slate-400 mb-1">Age</label>
              <input v-model.number="editForm.age" type="number" class="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-indigo-500" required />
            </div>
          </div>

          <div class="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
            <button type="button" @click="showEditModal = false" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium rounded-lg">
              Cancel
            </button>
            <button type="submit" :disabled="updating" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium rounded-lg disabled:opacity-50">
              {{ updating ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>

<!-- Modal create new account for admin-->
<div v-if="showCreateAdminModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
  <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 w-full max-w-md space-y-4 shadow-2xl">
    <div class="flex justify-between items-center border-b border-slate-800 pb-3">
      <h3 class="text-lg font-bold text-white">Create New Admin</h3>
      <button @click="showCreateAdminModal = false" class="text-slate-400 hover:text-white">✕</button>
    </div>
    
    <form @submit.prevent="handleCreateAdmin" class="space-y-3">
      <div class="grid grid-cols-2 gap-2">
        <div>
          <label class="block text-xs font-medium text-slate-400 mb-1">First Name</label>
          <input v-model="adminForm.first_name" placeholder="John" required class="w-full p-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-indigo-500" />
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-400 mb-1">Last Name</label>
          <input v-model="adminForm.last_name" placeholder="Doe" required class="w-full p-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-indigo-500" />
        </div>
      </div>

      <div>
        <label class="block text-xs font-medium text-slate-400 mb-1">Email</label>
        <input v-model="adminForm.email" type="email" placeholder="admin@example.com" required class="w-full p-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-indigo-500" />
      </div>

      <div class="grid grid-cols-2 gap-2">
        <div>
          <label class="block text-xs font-medium text-slate-400 mb-1">Phone</label>
          <input v-model="adminForm.phone" placeholder="+96170123456" required class="w-full p-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-indigo-500" />
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-400 mb-1">City</label>
          <input v-model="adminForm.city" placeholder="Beirut" required class="w-full p-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-indigo-500" />
        </div>
      </div>

      <div class="grid grid-cols-2 gap-2">
        <div>
          <label class="block text-xs font-medium text-slate-400 mb-1">Age</label>
          <input v-model.number="adminForm.age" type="number" placeholder="25" required class="w-full p-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-indigo-500" />
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-400 mb-1">Password</label>
          <input v-model="adminForm.password" type="password" placeholder="••••••••" required class="w-full p-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-indigo-500" />
        </div>
      </div>

      <div class="flex justify-end gap-2 pt-4 border-t border-slate-800">
        <button type="button" @click="showCreateAdminModal = false" class="px-4 py-2 text-slate-400 hover:text-white text-sm">Cancel</button>
        <button type="submit" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm font-medium">Create Admin</button>
      </div>
    </form>
  </div>
</div>

</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

definePageMeta({
  middleware: 'auth'
})

const { fetchApi } = useApi()
const user = ref(null)
const usersList = ref([])
const loading = ref(true)

const searchQuery = ref('')
const filterType = ref('all')

const stats = reactive({
  userCount: null,
  averageAge: null,
  topCities: ''
})

const showEditModal = ref(false)
const updating = ref(false)
const editForm = reactive({
  first_name: '',
  last_name: '',
  phone: '',
  city: '',
  age: 0
})

const filteredUsersList = computed(() => {
  return usersList.value.filter(u => {
    const fullName = `${u.first_name || ''} ${u.last_name || ''}`.toLowerCase()
    const email = (u.email || '').toLowerCase()
    const query = searchQuery.value.toLowerCase()

    const matchesSearch = fullName.includes(query) || email.includes(query)
    const matchesRole = filterType.value === 'all' || (u.type || u.role) === filterType.value

    return matchesSearch && matchesRole
  })
})

const loadUserData = async () => {
  try {
    user.value = await fetchApi('/users/me')
    
    const currentRole = user.value?.type || user.value?.role
    if (currentRole === 'admin') {
      await loadAnalytics()
      await loadUsersList()
    }
  } catch (error) {
    console.error('Failed to load user', error)
  } finally {
    loading.value = false
  }
}

const loadAnalytics = async () => {
  try {
    // 1. User Count Parsing
    const countRes = await fetchApi('/stats/stats/count')
    if (typeof countRes === 'object' && countRes !== null) {
      stats.userCount = countRes.total_users ?? countRes.count ?? countRes.total ?? JSON.stringify(countRes)
    } else {
      stats.userCount = countRes
    }

    // 2. Average Age Parsing
    const ageRes = await fetchApi('/stats/stats/average-age')
    if (typeof ageRes === 'object' && ageRes !== null) {
      const val = ageRes.average_age ?? ageRes.avg ?? ageRes.age
      stats.averageAge = typeof val === 'number' ? val.toFixed(1) : val
    } else {
      stats.averageAge = ageRes
    }

    // 3. Top Cities Parsing
    const citiesRes = await fetchApi('/stats/stats/top-cities')
    if (Array.isArray(citiesRes)) {
      stats.topCities = citiesRes.map(item => {
        if (typeof item === 'object' && item !== null) {
          return item.city || item._id || item.name || Object.values(item)[0]
        }
        return item
      }).filter(Boolean).join(', ')
    } else if (typeof citiesRes === 'object' && citiesRes !== null) {
      const list = citiesRes.top_cities || citiesRes.cities || citiesRes.items
      if (Array.isArray(list)) {
        stats.topCities = list.map(item => typeof item === 'object' ? (item.city || item._id || item.name) : item).join(', ')
      } else {
        stats.topCities = JSON.stringify(citiesRes)
      }
    } else {
      stats.topCities = citiesRes
    }
  } catch (error) {
    console.error('Failed to load stats', error)
  }
}

const openEditModal = () => {
  if (user.value) {
    editForm.first_name = user.value.first_name || ''
    editForm.last_name = user.value.last_name || ''
    editForm.phone = user.value.phone || ''
    editForm.city = user.value.city || ''
    editForm.age = user.value.age || 0
  }
  showEditModal.value = true
}

const handleUpdateProfile = async () => {
  updating.value = true
  try {
    await fetchApi('/users/me', {
      method: 'PUT',
      body: JSON.stringify(editForm)
    })
    showEditModal.value = false
    await loadUserData()
  } catch (error) {
    alert(error.message || 'Failed to update profile')
  } finally {
    updating.value = false
  }
}

const loadUsersList = async () => {
  try {
    const res = await fetchApi('/users/')
    usersList.value = Array.isArray(res) ? res : (res.items || res.users || [])
  } catch (error) {
    console.error('Failed to load users list', error)
  }
}

const handleDeleteUser = async (userId) => {
  if (!confirm('Are you sure you want to delete this user?')) return

  try {
    await fetchApi(`/users/${userId}`, {
      method: 'DELETE'
    })
    await loadUsersList()
    await loadAnalytics()
  } catch (error) {
    alert(error.message || 'Failed to delete user')
  }
}

const handleLogout = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('access_token')
  }
  navigateTo('/login')
}

const showCreateAdminModal = ref(false)

const adminForm = reactive({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  city: '',
  age: 25,
  password: ''
})

const handleCreateAdmin = async () => {
  try {
    const payload = {
      first_name: adminForm.first_name,
      last_name: adminForm.last_name,
      email: adminForm.email,
      phone: adminForm.phone,
      city: adminForm.city,
      age: Number(adminForm.age),
      password: adminForm.password
    }

    // send the request with ensure that body as JSON
    await fetchApi('/auth/register/admin', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    alert('Admin created successfully!')
    showCreateAdminModal.value = false

    // release the sample
    adminForm.first_name = ''
    adminForm.last_name = ''
    adminForm.email = ''
    adminForm.phone = ''
    adminForm.city = ''
    adminForm.age = 25
    adminForm.password = ''

    await loadUsersList()
    await loadAnalytics()
  } catch (error) {
    console.error('Failed to create admin:', error)
    alert('Failed to create admin. Please check values.')
  }
}
onMounted(() => {
  loadUserData()
})
</script>