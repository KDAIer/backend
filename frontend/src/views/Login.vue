<template>
  <div class="login-container">
    <div class="login-form">
      <h2>智能家居系统</h2>
      <form @submit.prevent="handleLogin">
        <!-- 用户名 -->
        <div class="form-group">
          <label>用户名</label>
          <input 
            type="text"
            v-model="username"
            placeholder="请输入用户名"
            required
          />
        </div>

        <!-- 密码 -->
        <div class="form-group">
          <label>密码</label>
          <input 
            type="password"
            v-model="password"
            placeholder="请输入密码"
            required
            minlength="6"
          />
        </div>

        <!-- 错误提示 -->
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <!-- 登录按钮 -->
        <button type="submit" :disabled="isLoading">
          {{ isLoading ? '登录中...' : '登录' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

const handleLogin = () => {
  // 简单表单验证
  if (!username.value || !password.value) {
    errorMessage.value = '请填写所有字段'
    return
  }

  // 模拟 API 请求
  isLoading.value = true
  errorMessage.value = ''

  setTimeout(() => {
    // 这里应该调用真实的后端接口
    if (username.value === 'admin' && password.value === '123456') {
      // 登录成功，存储 token（实际应使用 Vuex/Pinia）
      localStorage.setItem('authToken', 'demo-token')
      router.push('/') // 需要先创建 dashboard 页面
    } else {
      errorMessage.value = '用户名或密码错误'
    }
    isLoading.value = false
  }, 1000)
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f0f2f5;
}

.login-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  width: 350px;
}

h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.2rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #4a5568;
}

input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 1rem;
}

button {
  width: 100%;
  padding: 1rem;
  background: #3182ce;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: opacity 0.2s;
}

button:hover:not(:disabled) {
  opacity: 0.9;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  color: #dc2626;
  margin-top: 1rem;
  text-align: center;
}
</style>