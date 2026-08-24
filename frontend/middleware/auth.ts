export default defineNuxtRouteMiddleware(async (to, from) => {
  // verify that the code is work in browser(Client-side)
  if (typeof window === 'undefined') return

  const token = localStorage.getItem('access_token')

  // if there is no tokern transfer the client to Login
  if (!token) {
    return navigateTo('/login')
  }

  // if the token exist .. verify from expirtory of user
  try {
    const { fetchApi } = useApi()
    const user = await fetchApi('/users/me')

    // protect admin pages (if the role wanted admin)
    if (to.meta.requiresAdmin && user.role !== 'admin') {
      return navigateTo('/')
    }
  } catch (error) {
    //  in case of ending for exraire or errors occur .. delete the token and return to Login
    localStorage.removeItem('access_token')
    return navigateTo('/login')
  }
})