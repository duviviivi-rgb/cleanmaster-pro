<template>
  <div id="app">
    <el-container style="height: 100vh;">
      <el-header height="60px">
        <div class="header-content">
          <h1>检验批容量与隐蔽工程报告生成系统</h1>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px" style="background-color: #f5f7fa;">
          <el-menu
            :default-active="activeMenu"
            class="el-menu-vertical-demo"
            router
          >
            <el-menu-item index="/">
              <span>首页</span>
            </el-menu-item>
            <el-menu-item index="/file-process">
              <span>文件处理</span>
            </el-menu-item>
            <el-menu-item index="/material-edit">
              <span>材料编辑</span>
            </el-menu-item>
            <el-menu-item index="/report-preview">
              <span>报告预览</span>
            </el-menu-item>
            <el-menu-item index="/config">
              <span>配置管理</span>
            </el-menu-item>
            <el-menu-item index="/history">
              <span>历史记录</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: Arial, sans-serif;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 20px;
}

.header-content h1 {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.el-menu-vertical-demo {
  height: 100%;
}

.el-main {
  padding: 20px;
  background-color: #f0f2f5;
}
</style>
