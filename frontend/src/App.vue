<script setup>
import { RouterView, useRoute } from 'vue-router'
import { onMounted, ref, watch } from 'vue'
import { isLoggedIn, currentUsername, authReady, transitionName } from './auth.js'
import { API } from './config.js'
const route = useRoute()

watch (() => route.path, (newPath) => {
  if (newPath === '/') {
    transitionName.value = 'fade-up'
  } else {
    transitionName.value = 'fade-down'
  }
})

onMounted(async () => {
  try {
    const response = await fetch(`${API}/auth/me`, {
      credentials: "include"
    })
    if (response.ok) {
      const data = await response.json()
      isLoggedIn.value = true
      currentUsername.value = data.username
    } else {
      isLoggedIn.value = false
    }
  } catch (err) {
    isLoggedIn.value = false
  } finally {
    authReady.value = true
  }
})
</script>

<template>
  <div v-if="!authReady" class="auth-loading"></div>
  <div v-else class="router-wrapper">
    <RouterView v-slot=" {Component}">
      <Transition :name="transitionName">
        <component :is="Component" :key="$route.path"/>
      </Transition>
    </RouterView>
  </div>
</template>

<style>
</style>