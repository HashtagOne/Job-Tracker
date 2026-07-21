<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { API } from '../config.js'
const router = useRouter()

const username = ref("")
const password = ref("")
const error = ref("")
const loading = ref(false)
const confirmPassword = ref("")

async function register() {
    error.value = ""
    loading.value = true

    try {

        if (password.value !== confirmPassword.value) {
            error.value = "Passwords do not match."
            loading.value = false
            return
        }

        const response = await fetch(`${API}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json"}, 
            credentials: "include",
            body: JSON.stringify({
                username: username.value,
                password: password.value
            })
        })

        const data = await response.json()

        if (!response.ok) {
            error.value = data.error
            return
        }

        router.push("/login")
    } catch (err) {
        error.value = "Something went wrong. Please try again."
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="auth-container">
        <div class="auth-card">
            <div class="auth-header">
                <h1>Hello, future <br><span class="accent-text">Job Hunter.</span></h1>
                <p> Register now to start listing your applications.</p>
            </div>

            <div class="auth-fields">
                <div class="field">
                    <label>Username</label>
                    <input
                        v-model="username"
                        type="text"
                        placeholder="Username"
                        @keydown.enter="register"
                        autocomplete="off"
                    />
                </div>
                <div class="field">
                    <label>Password</label>
                    <input
                        v-model="password"
                        type="password"
                        placeholder="Password"
                        @keydown.enter="register"
                        autocomplete="new-password"
                    />
                </div>
                <div class="field">
                    <label>Confirm Password</label>
                    <input
                        v-model="confirmPassword"
                        type="password"
                        placeholder="Confirm Password"
                        @keydown.enter="register"
                        autocomplete="new-password"
                    />
                </div>
            </div>
            
            <p v-if="error" class="auth-error"> {{ error  }}</p>

            <button @click="register" :disabled="loading">
                {{  loading ? "Registering.." : "Register" }}
            </button>

            <p class="auth-switch">
                Already have an account?
                <RouterLink to="/login">Login Here </RouterLink>
            </p>
        </div>
    </div>
</template>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-primary);
}

.auth-card {
  background: var(--bg-card);
  border-radius: 16px;
  padding: 40px;
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  border: 0.5px solid var(--border);
  box-shadow:
  0 0 0 1px rgba(91, 140, 255, 0.6),
  0 0 32px rgba(91, 140, 255, 0.2);
}

.auth-header h1 {
  font-size: 1.8rem;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 4px;
  font-family: 'Space Grotesk', sans-serif;
}

.accent-text {
  font-weight: 700;
  font-family: 'Bricolage Grotesque', sans-serif;
  color: var(--color-blue);
}


.auth-header p {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.auth-fields {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05rem;
}

input {
  padding: 10px 14px;
  border: 0.5px solid var(--border);
  border-radius: 8px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-family: 'DM Sans', sans-serif;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s;
}

input:focus {
  border-color: var(--color-blue);
  box-shadow: 0 0 0 3px rgba(59,109,17,0.1);
}

button {
  background: var(--color-blue);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px;
  font-family: "DM Sans", sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.1s;
  width: 100%;
}

button:hover {
  opacity: 0.9
}

button:active {
  transform: scale(0.98);
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.auth-switch a {
  color: var(--color-blue);
  text-decoration: none; 
  font-weight: 600;
}

.auth-switch {
  text-align: center;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.auth-switch a:hover {
  text-decoration: none;
}


a {
  position: relative;
  text-decoration: none;
}

a::after {
  content: '';
  position: absolute;
  bottom: 1.5px;
  left: 0;
  width: 0;
  height: 1.5px;
  background: var(--color-blue);
  transition: width 0.3s ease;
}

a:hover::after {
  width: 100%;
}
</style>