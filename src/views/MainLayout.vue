<template>
    <div id="app">
      <el-container>
        <el-aside :width="isSidebarCollapsed ? '40px' : '500px'">
          <Sidebar @toggle-sidebar="handleSidebarToggle" />
        </el-aside>
        <el-container>
          <el-main>
            <Content />
          </el-main>
          <el-footer>
            <Footer />
          </el-footer>
        </el-container>
      </el-container>
    </div>
  </template>
  
  <script>
  import Sidebar from '../components/AppSidebar.vue';
  import Content from '../components/AppContent.vue';
  import Footer from '../components/AppFooter.vue';
  
  export default {
    name: 'App',
    components: {
      Sidebar,
      Content,
      Footer
    },
    data() {
      return {
        isSidebarCollapsed: false // 添加状态变量
      };
    },
    methods: {
      handleSidebarToggle(collapsed) {
        this.isSidebarCollapsed = collapsed;
      }
    }
  };
  </script>
  
  <style scoped>
  .el-aside {
    background-color: rgba(255, 255, 255, 0.5);
    color: rgb(9, 9, 9);
    padding-top: 10px;
    transition: width 0.3s ease, height 0.3s ease;
    position: relative;
    overflow: hidden;
  }
  
  .el-main {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: rgba(255, 255, 255, 0.8);
    margin: 10px 10px;
    overflow: auto;
    padding: 10px;
    box-sizing: border-box;
    transition: margin-left 0.3s ease; 
    border-radius: 10px;
  }
  
  .el-footer {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 10px 10px;
    padding: 10px;
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 10px;
  }
  </style>