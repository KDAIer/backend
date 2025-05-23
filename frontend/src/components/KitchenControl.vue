<template>
  <div class="kitchen-panel">
    <div class="panel-header">
      <h2>厨房控制中心</h2>
      <button class="close-btn" @click="$emit('close')">×</button>
    </div>

    <div class="control-section">
      <div class="section-title">🍳 大家电</div>
      <div class="device-grid">
        <div class="device-card" v-for="device in largeAppliances" :key="device.name">
          <font-awesome-icon :icon="device.icon" class="device-icon" />
          <div class="device-name">{{ device.name }}</div>
          <div v-if="device.name === '智能冰箱'" class="stock-status">
            <font-awesome-icon icon="box" class="stock-icon" />
            <span :class="{ 'low-stock': device.stock < 3 }">库存：{{ device.stock }}件</span>
          </div>
          <div v-if="device.name === '智能烤箱'" class="recipe-select">
            <button @click="chooseRecipe(device)">🍽️ {{ device.recipe || '选择菜谱' }}</button>
          </div>
          <button
            class="toggle-btn"
            :class="{ active: device.status }"
            @click="device.status = !device.status"
          >
            {{ device.status ? '运行中' : '待机' }}
          </button>
        </div>
      </div>

      <div class="section-title">🍴 小家电</div>
      <div class="device-grid">
        <div class="device-card" v-for="device in smallAppliances" :key="device.name">
          <font-awesome-icon :icon="device.icon" class="device-icon" />
          <div class="device-name">{{ device.name }}</div>
          <button
            class="toggle-btn"
            :class="{ active: device.status }"
            @click="device.status = !device.status"
          >
            {{ device.status ? '运行中' : '待机' }}
          </button>
        </div>
      </div>

      <div class="section-title">🛡️ 安防</div>
      <div class="sensor-grid">
        <div
          class="sensor-card"
          v-for="sensor in sensors"
          :key="sensor.name"
          :class="{ alert: sensor.status !== 'normal' }"
        >
          <font-awesome-icon :icon="sensor.icon" class="sensor-icon" />
          <div class="sensor-name">{{ sensor.name }}</div>
          <div class="sensor-status">
            <span v-if="sensor.status === 'normal'">正常</span>
            <span v-else class="alert-text">⚠️ 报警中!</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
  faTemperatureLow,
  faWind,
  faHotTub,
  faSink,
  faBurn,
  faWater,
  faBox,
} from '@fortawesome/free-solid-svg-icons'

const largeAppliances = ref([
  { name: '智能冰箱', status: true, stock: 5, icon: faTemperatureLow },
  { name: '智能烤箱', status: false, recipe: '', icon: faHotTub },
  { name: '洗碗机', status: false, icon: faSink },
])

const smallAppliances = ref([
  { name: '电饭煲', status: false, icon: faHotTub },
  { name: '电磁炉', status: false, icon: faHotTub },
  { name: '抽油烟机', status: false, icon: faWind },
])

const sensors = ref([
  { name: '燃气泄漏传感器', status: 'normal', icon: faBurn },
  { name: '水浸传感器', status: 'alert', icon: faWater },
])

const chooseRecipe = (device) => {
  const recipes = ['烤鸡', '披萨', '蛋挞']
  const choice = prompt('请选择菜谱：\n' + recipes.join('\n'))
  if (recipes.includes(choice)) {
    device.recipe = choice
  }
}
</script>

<style scoped>
.kitchen-panel {
  width: 500px;
  padding: 1.2rem;
  background-color: #f9f9f9;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', sans-serif;
  margin: 0 auto;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.2rem;
  padding-bottom: 0.8rem;
  border-bottom: 1px solid #e0e0e0;
}

.panel-header h2 {
  font-size: 1.3rem;
  margin: 0;
  color: #37474f;
}

.close-btn {
  font-size: 2.5rem;
  line-height: 1;
  padding: 0 0.6rem;
  background: none;
  border: none;
  cursor: pointer;
  color: #666;
  transition: all 0.2s;
  border-radius: 50%;
}

.close-btn:hover {
  color: #ce3c31;
  background: #f0f0f0;
}

.control-section {
  display: grid;
  gap: 1.5rem;
}

.section-title {
  font-size: 1.1rem;
  font-weight: bold;
  margin: 0 0 0.8rem;
  color: #37474f;
  padding-left: 0.5rem;
  border-left: 3px solid #42a5f5;
}

.device-grid,
.sensor-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
}

.device-card,
.sensor-card {
  background-color: #fff;
  padding: 1rem;
  border-radius: 12px;
  text-align: center;
  border: 1px solid #e0e0e0;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.2s;
}

.device-card:hover,
.sensor-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.device-icon,
.sensor-icon {
  font-size: 1.6rem;
  color: #607d8b;
  margin-bottom: 0.6rem;
}

.device-name,
.sensor-name {
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.toggle-btn {
  margin-top: 0.6rem;
  background-color: #b0bec5;
  color: white;
  border: none;
  padding: 0.4rem 0.8rem;
  font-size: 0.8rem;
  border-radius: 15px;
  cursor: pointer;
  transition: all 0.3s;
  width: 80%;
}

.toggle-btn.active {
  background-color: #4caf50;
}

.toggle-btn:hover {
  opacity: 0.9;
}

.stock-status {
  font-size: 0.8rem;
  margin: 0.5rem 0;
  color: #444;
}

.low-stock {
  color: #d32f2f;
  font-weight: bold;
}

.recipe-select button {
  margin: 0.5rem 0;
  background-color: #fffde7;
  border: 1px solid #ffb300;
  padding: 0.4rem 0.8rem;
  font-size: 0.8rem;
  border-radius: 12px;
  color: #f57f17;
  cursor: pointer;
  transition: all 0.2s;
}

.recipe-select button:hover {
  background-color: #fff8e1;
}

.sensor-card.alert {
  background-color: #ffebee;
  border: 1px solid #e53935;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.02);
  }
  100% {
    transform: scale(1);
  }
}

.sensor-status {
  font-size: 0.8rem;
}

.alert-text {
  color: #e53935;
  font-weight: bold;
}
</style>
