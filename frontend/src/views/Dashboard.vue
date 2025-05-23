<template>
  <div class="dashboard">
    <!-- 头部 -->
    <header class="header">
      <h1>智能家居控制中心</h1>
      <div class="user-info">
        <span>当前用户：{{ username }}</span>
        <button @click="logout" class="logout-btn">退出登录</button>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 顶部区域 -->
      <div class="top-row">
        <!-- 左上快速控制 -->
        <section class="quick-control card">
          <h2>快速控制</h2>
          <div class="device-grid">
            <div
              class="device-card"
              v-for="(device, index) in quickDevices"
              :key="index"
              :class="{ 'device-on': device.state }"
            >
              <div class="device-icon">
                <font-awesome-icon :icon="device.icon" class="device-icon" />
              </div>
              <div class="device-info">
                <h3>{{ device.name }}</h3>
                <p class="device-status">{{ device.status }}</p>
              </div>
              <!-- 修改后 -->
              <div class="device-control">
                <button
                  class="control-btn"
                  @click.stop="handleDeviceAction(device)"
                  :disabled="device.type === 'emergency'"
                >
                  <span class="toggle-icon">
                    {{ device.state ? '●' : '○' }}
                  </span>
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- 右上区域控制 -->
        <section class="area-control card">
          <h2>区域控制</h2>

          <!-- 四宫格区域选择 -->
          <div class="grid-area-selector" ref="gridItems">
            <div
              class="grid-area-item"
              v-for="(area, index) in areas"
              :key="index"
              @click="toggleArea(area.id)"
              :class="{
                active: activeArea === area.id,
                'has-sub': area.children,
              }"
            >
              <!-- 图标 -->
              <font-awesome-icon :icon="area.icon" class="area-icon" />

              <!-- 文字 -->
              <span class="area-name">{{ area.name }}</span>
            </div>
          </div>

          <!-- 区域详细控制 -->
          <div class="area-details" v-if="activeArea" @click.self="activeArea = null">
            <component
              :is="getAreaComponent(activeArea)"
              @close="activeArea = null"
              class="modal-content"
            />
          </div>
        </section>
      </div>

      <!-- 底部区域 -->
      <div class="bottom-row">
        <!-- 左下环境监测 -->
        <section class="environment card">
          <h2>环境监测</h2>
          <div class="data-grid">
            <template v-for="(data, key) in environmentData" :key="key">
              <!-- 特殊样式的时间项 -->
              <div class="data-card" :class="{ 'time-card': key === 'time' }" v-if="key === 'time'">
                <div class="data-label">{{ data.label }}</div>
                <div class="data-value time-value">{{ data.value }}</div>
              </div>

              <!-- 常规数据项 -->
              <div class="data-card" v-else>
                <div class="data-label">{{ data.label }}</div>
                <div class="data-value">{{ data.value }}</div>
              </div>
            </template>
          </div>
        </section>

        <!-- 右下智能场景 -->
        <section class="scenes card">
          <h2>智能场景</h2>
          <div class="scene-grid">
            <button
              v-for="(scene, index) in scenes"
              :key="index"
              class="scene-btn"
              @click="activateScene(scene.id)"
            >
              <span class="scene-icon">{{ scene.icon }}</span>
              {{ scene.name }}
            </button>
          </div>
        </section>
      </div>
    </main>
  </div>

  <Teleport to="body">
    <div v-if="networkModalVisible" class="network-modal">
      <div class="modal-content">
        <h3>网络设置</h3>
        <div class="network-info">
          <p>当前连接：家庭Wi-Fi_5G</p>
          <p>信号强度：<span class="strength-bar" style="--strength: 80%"></span></p>
        </div>
        <button class="btn" @click="networkModalVisible = false">关闭</button>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import AirConditioner from '@/components/AirConditioner.vue'
import LivingRoomControl from '@/components/LivingRoomControl.vue'
import KitchenControl from '@/components/KitchenControl.vue'
import BedroomControl from '@/components/BedroomControl.vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
  faFan,
  faHouse,
  faUtensils,
  faBed,
  faPowerOff,
  faLock,
  faShieldAlt,
  faExclamationTriangle,
  faWifi,
} from '@fortawesome/free-solid-svg-icons'

// 模拟用户数据
const username = ref('管理员')
const activeArea = ref(null)

// 区域配置数据
const areas = ref([
  {
    id: 'ac',
    name: '空调控制',
    icon: faFan,
    component: 'AirConditioner',
  },
  {
    id: 'living',
    name: '客厅',
    icon: faHouse,
    component: 'LivingRoomControl',
  },
  {
    id: 'kitchen',
    name: '厨房',
    icon: faUtensils,
    component: 'KitchenControl',
  },
  {
    id: 'bedroom',
    name: '卧室',
    icon: faBed,
    component: 'BedroomControl',
  },
])

// 快速控制设备
// 修改后的 quickDevices 数组
const quickDevices = ref([
  {
    id: 1,
    name: '总控开关',
    state: true,
    status: '系统在线',
    icon: faPowerOff, // 使用已导入的图标
    type: 'master',
  },
  {
    id: 2,
    name: '智能门锁',
    state: false,
    status: '已锁定',
    icon: faLock,
    type: 'lock',
  },
  {
    id: 3,
    name: '安防系统',
    state: true,
    status: '布防中',
    icon: faShieldAlt,
    type: 'security',
  },
  {
    id: 4,
    name: '紧急报警',
    state: false,
    status: '待机状态',
    icon: faExclamationTriangle, // 修正图标
    type: 'emergency',
  },
  {
    id: 5,
    name: '网络状态',
    state: true,
    status: '5G在线',
    icon: faWifi,
    type: 'network',
  },
])

// 1. 创建响应式时间源
const currentTime = ref('')

// 2. 计时器逻辑封装
function startTimeUpdater() {
  const update = () => {
    currentTime.value = new Date().toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    })
  }

  update() // 立即执行一次
  const timer = setInterval(update, 1000)

  onUnmounted(() => {
    clearInterval(timer)
  })
}

// 环境数据
const environmentData = ref({
  time: { label: '时间', value: computed(() => currentTime.value) },
  people: { label: '屋内有', value: '3人' },
  temperature: { label: '温度', value: '22°C' },
  humidity: { label: '湿度', value: '57%' },
  pm25: { label: 'PM2.5', value: '32 μg/m³' },
  co2: { label: '二氧化碳', value: '450 ppm' },
})
onMounted(startTimeUpdater)
// 场景模式
const scenes = ref([
  { id: 'home', name: '回家模式', icon: '🏠' },
  { id: 'away', name: '离家模式', icon: '🚪' },
  { id: 'sleep', name: '睡眠模式', icon: '🛌' },
])

// 切换区域
const toggleArea = (areaId) => {
  activeArea.value = activeArea.value === areaId ? null : areaId
}

// 获取对应区域的组件
const getAreaComponent = (areaId) => {
  const componentMap = {
    ac: AirConditioner,
    living: LivingRoomControl,
    kitchen: KitchenControl,
    bedroom: BedroomControl,
  }
  return componentMap[areaId]
}

// 设备控制方法
// 新增状态更新方法
const handleDeviceAction = (device) => {
  switch (device.type) {
    case 'master':
      toggleGeneralSwitch(device)
      break
    case 'lock':
      toggleLock(device)
      break
    case 'security':
      toggleSecurity(device)
      break
    case 'emergency':
      if (device.state) {
        if (confirm('确定要取消紧急报警吗？')) {
          cancelEmergency(device)
        }
      } else {
        if (confirm('⚠️ 确认触发紧急报警？')) {
          triggerEmergency(device)
        }
      }
      break
    case 'network':
      showNetworkModal(device)
      break
  }
}

// 具体控制逻辑
const toggleGeneralSwitch = (device) => {
  device.state = !device.state
  device.status = device.state ? '系统在线' : '系统离线'
}

const toggleLock = (device) => {
  device.state = !device.state
  device.status = device.state ? '已锁定 - 最后操作：' + new Date().toLocaleTimeString() : '已解锁'
}

const toggleSecurity = (device) => {
  device.state = !device.state
  device.status = device.state ? '布防中' : '撤防中'
  if (device.state) {
    alert('安防系统已激活，检测到异常会发送通知')
  }
}

// 完善后的紧急报警逻辑
let emergencyTimeout
const triggerEmergency = (device) => {
  if (device.state) return // 防止重复触发
  device.state = true
  device.status = '报警已触发（10秒后自动通知警方）'

  emergencyTimeout = setTimeout(() => {
    if (device.state) {
      // 确保状态未被取消
      alert('⚠️ 紧急报警已触发！安保人员正在赶来')
      device.state = false // 自动复位
      device.status = '待机状态'
    }
  }, 10000)
}

const cancelEmergency = (device) => {
  device.state = false
  device.status = '待机状态'
  clearTimeout(emergencyTimeout) // 清理定时器
}

// 新增网络控制弹窗逻辑
const networkModalVisible = ref(false)
const showNetworkModal = () => {
  networkModalVisible.value = true
}

// const triggerEmergency = (device) => {
//   device.state = !device.state;
//   device.status = device.state ? '已触发！' : '待机状态';
//   if(device.state) {
//     alert('⚠️ 紧急报警已触发！安保人员正在赶来');
//   }
// };

// 退出登录
const logout = () => {
  localStorage.removeItem('authToken')
  window.location.href = '/login'
}
</script>

<style scoped>
/* 基础布局 */
.dashboard {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: #2c3e50;
  color: white;
}

.main-content {
  display: grid;
  grid-template-rows: auto auto;
  gap: 2rem;
  padding: 2rem;
  flex: 1;
}

/* 卡片布局 */
.card {
  background: rgb(217, 239, 241);
  padding: 1rem;
  border-radius: 16px;
  /* width: 800px; */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

/* 顶部双列布局 */
.top-row {
  display: grid;
  grid-template-columns: 700px 400px 200px;
  gap: 2rem;
}

/* 底部双列布局 */
.bottom-row {
  display: grid;
  grid-template-columns: 700px 400px 200px;
  gap: 2rem;
}

/* 快速控制设备 */
.device-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

/* 新增状态颜色 */
.device-online {
  color: #28a745;
}
.device-offline {
  color: #dc3545;
}
.device-warning {
  color: #ffc107;
}

/* 根据设备类型设置图标颜色 */
.device-card.master .device-icon {
  color: #3182ce; /* 蓝色 */
}
.device-card.lock .device-icon {
  color: #6f42c1; /* 紫色 */
}
.device-card.emergency .device-icon {
  color: #dc3545; /* 红色 */
}
.device-card.network .device-icon {
  color: #38a169; /* 绿色 */
}

.device-card {
  display: flex;
  align-items: center;
  padding: 1.2rem;
  border-radius: 12px;
  background: #f8fafc;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #e2e8f0;
  position: relative;
}

.device-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border-color: #3182ce;
}

/* 设备状态指示灯 */
.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 1rem;
  flex-shrink: 0;
}

/* 不同状态的颜色 */
.state-on {
  background: #38bdf8;
}
.state-off {
  background: #94a3b8;
}
.state-error {
  background: #ef4444;
}

/* 控制按钮统一样式 */
.control-group {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-left: auto;
}

/* 紧急报警特殊样式 */
.emergency .device-card {
  border-color: #ef4444;
  background: #fff5f5;
}

.device-on {
  background: #e3f2fd;
}

.device-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #3182ce;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
}

.device-status {
  color: #666;
  font-size: 0.9rem;
  margin: 0.5rem 0;
}

/* 区域控制样式 */

.area-control {
  /* 增加高度以确保四宫格布局良好显示 */
  max-height: 380px;
  overflow: hidden;
}

.grid-area-selector {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  transition: height 0.3s ease;
}

.grid-area-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem;
  padding: 1.2rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  text-align: center;
  background-color: #f8fafc;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  min-width: 100px;
}

.grid-area-item:hover {
  background: #a4c8f1;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.grid-area-item.active {
  background: #e3f2fd;
  border: 2px solid #3182ce;
  transform: scale(1.05);
  z-index: 1;
}

.area-icon {
  width: 36px;
  height: 36px;
  color: #666;
  flex-shrink: 0;
  margin-bottom: 0.5rem;
}

.area-icon svg {
  font-size: 24px; /* 增大图标尺寸 */
}

.grid-area-item.active .area-icon {
  color: #3182ce;
}

.area-name {
  font-size: 1.2rem;
  color: #4a5568;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.area-details {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  position: relative;
  z-index: 1001;
  max-height: 90vh;
  overflow-y: auto;
}

/* 环境监测 */
.data-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.data-card {
  padding: 1rem;
  border-radius: 8px;
  background: #f8fafc;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.data-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border-color: #539ce0;
}
/* 时间特殊样式 */
.time-card {
  grid-column: span 1;
  background: #e6f7ff;
}

.time-value {
  font-size: 1.5rem;
  color: #1890ff;
}

/* 人数特殊样式 */
.people-count {
  font-weight: bold;
  color: #ff4d4f;
}

.data-label {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.3rem;
}

.data-value {
  font-size: 1.3rem;
  font-weight: bold;
  color: #2c3e50;
}

/* 智能场景 */
.scene-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.scene-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.scene-btn:hover {
  border-color: #3182ce;
  background: #f0f7ff;
}

.scene-icon {
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
}

/* 新增在 <style scoped> 中 */
.air-conditioner {
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
}

.temp-display {
  text-align: center;
  margin-bottom: 1.5rem;
}

.current-temp {
  font-size: 3rem;
  color: #2c3e50;
  font-weight: bold;
}

.toggle-btn {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #e3f2fd;
  border: none;
  color: #3182ce;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.temp-control {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.temp-control button {
  width: 40px;
  height: 40px;
  border: 1px solid #e2e8f0;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.mode-switch {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.mode-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  cursor: pointer;
}

.mode-btn.active {
  border-color: #3182ce;
  background: #e3f2fd;
}
</style>
