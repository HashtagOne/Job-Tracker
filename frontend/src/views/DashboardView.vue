<script setup>
import {ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { isLoggedIn, currentUsername, transitionName} from '../auth.js'
import { API } from '../config.js'

const router = useRouter()
const jobs = ref([])
const loading = ref(true)

async function loadJobs() {
  try {
    const response = await fetch(`${API}/jobs`, {
      credentials: "include"
    })

    if (response.status === 401) {
      isLoggedIn.value = false
      router.push("/login")
      return
    }
    
    const data = await response.json()
    jobs.value = data
    console.log(jobs.value)

  } catch (err) {
    console.error("Failed to load jobs", err)
  } finally {
    loading.value = false
  }
}

async function logOut() {
  await fetch(`${API}/auth/logout`, {
    method: "POST",
    credentials: "include"
  })
  isLoggedIn.value = false
  currentUsername.value = ""
  transitionName.value = 'fade-down'
  router.push("/login")
}

onMounted(() => {
  loadJobs()
})
</script>

<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1> Job Tracker</h1>
      <div class="header-right">
        <span class="username"> {{ currentUsername }}</span>
        <button class="logout-btn" @click="logOut">Log Out</button>
      </div>
    </header>
  </div>
</template>