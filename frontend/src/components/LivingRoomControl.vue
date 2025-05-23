<template>
  <div class="living-room-panel">
    <div class="panel-header">
      <h2>客厅控制</h2>
      <button class="close-btn" @click="$emit('close')">×</button>
    </div>

    <div class="control-sections">
      <!-- 灯光控制 -->
      <section class="control-card">
        <h3 class="section-title">💡 灯光</h3>
        <div class="device-grid">
          <div
            v-for="(light, index) in lights"
            :key="index"
            class="device-item"
            :class="{ active: light.status }"
          >
            <div class="device-icon">{{ light.icon }}</div>
            <span class="device-name">{{ light.name }}</span>
            <button
              class="toggle-btn"
              :class="{ on: light.status }"
              @click="toggleDevice(light, 'lights')"
            >
              {{ light.status ? '开' : '关' }}
            </button>
          </div>
        </div>
      </section>

      <!-- 电器控制 -->
      <section class="control-card">
        <h3 class="section-title">📺 电器</h3>
        <div class="device-grid">
          <div
            v-for="(appliance, index) in appliances"
            :key="index"
            class="device-item"
            :class="{ active: appliance.status }"
          >
            <div class="device-icon">{{ appliance.icon }}</div>
            <span class="device-name">{{ appliance.name }}</span>
            <button
              class="toggle-btn"
              :class="{ on: appliance.status }"
              @click="toggleDevice(appliance, 'appliances')"
            >
              {{ appliance.status ? '开' : '关' }}
            </button>
          </div>
        </div>
      </section>

      <!-- 窗帘控制 -->
      <section class="control-card">
        <h3 class="section-title">🪟 窗帘</h3>
        <div class="curtain-control">
          <div class="slider-container">
            <input
              type="range"
              min="0"
              max="100"
              v-model="curtainPosition"
              class="curtain-slider"
            />
            <div class="percentage">{{ curtainPosition }}%</div>
          </div>
          <div class="curtain-btns">
            <button class="preset-btn" @click="setCurtain(0)">全关</button>
            <button class="preset-btn" @click="setCurtain(50)">半开</button>
            <button class="preset-btn" @click="setCurtain(100)">全开</button>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const lights = ref([
  { name: '主灯', icon: '💡', status: true },
  { name: '沙发灯', icon: '🛋', status: false },
  { name: '落地灯', icon: '🪔', status: false },
])

const appliances = ref([
  { name: '电视', icon: '📺', status: false },
  { name: '音响', icon: '🔊', status: false },
  { name: '空调', icon: '❄️', status: true },
])

const curtainPosition = ref(50)

const toggleDevice = (device, type) => {
  device.status = !device.status
}

const setCurtain = (value) => {
  curtainPosition.value = value
}
</script>

<style scoped>
.living-room-panel {
  width: 380px;
  padding: 1rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.panel-header h2 {
  font-size: 1.3rem;
  margin: 0;
}

.close-btn {
  font-size: 2.5rem;
  line-height: 1;
  padding: 0 0.5rem;
  background: none;
  border: none;
  cursor: pointer;
  color: #666;
  transition: all 0.2s;
}

.close-btn:hover {
  color: #ce3c31;
}

.control-sections {
  display: grid;
  gap: 1rem;
}

.control-card {
  background: #f8fafc;
  border-radius: 8px;
  padding: 1rem;
}

.section-title {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  color: #2c3e50;
}

.device-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.8rem;
}

.device-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.8rem 0.5rem;
  border-radius: 6px;
  background: white;
  border: 1px solid #e2e8f0;
}

.device-item.active {
  border-color: #3182ce;
  background: #e3f2fd;
}

.device-icon {
  font-size: 1.5rem;
  margin-bottom: 0.3rem;
}

.device-name {
  font-size: 0.8rem;
  margin-bottom: 0.5rem;
}

.toggle-btn {
  padding: 0.2rem 0.6rem;
  font-size: 0.7rem;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: white;
}

.toggle-btn.on {
  background: #3182ce;
  color: white;
  border-color: #3182ce;
}

.curtain-control {
  display: grid;
  gap: 0.8rem;
}

.curtain-slider {
  width: 100%;
  height: 6px;
}

.percentage {
  font-size: 1rem;
}

.curtain-btns {
  display: flex;
  justify-content: center;
  gap: 0.8rem;
}

.preset-btn {
  padding: 0.3rem 0.6rem;
  font-size: 0.8rem;
  border: 1px solid #e2e8f0;
}
</style>

<!-- 1. 整体结构变化
原代码（模态框）：
html
<div class="living-room-modal">
  <div class="modal-backdrop" @click="$emit('close')"></div>
  <div class="modal-content">

  </div>
</div>
修改后（直接嵌入）：
html
<div class="living-room-panel">

</div>
变化：移除了遮罩层和模态框层级结构，改为扁平化设计。

2. 尺寸与间距调整
原样式：
css
.modal-content {
  width: 600px;
  padding: 2rem;
  border-radius: 16px;
}
.device-item {
  padding: 1rem;
  margin-bottom: 0.8rem;
}
修改后：
css
.living-room-panel {
  width: 380px; /* 宽度缩小 */
  padding: 1rem; /* 内边距减小 */
  border-radius: 10px; /* 圆角缩小 */
}
.device-item {
  padding: 0.8rem 0.5rem; /* 内边距压缩 */
  margin-bottom: 0.5rem;
}
变化：所有尺寸按比例缩小约30%-40%。-->
