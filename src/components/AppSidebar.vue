<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <el-container :class="['main-sidebar', { collapsed: isSidebarCollapsed }]">
    <el-header class="header">
      <img v-if="!isSidebarCollapsed" src="../assets/img/favicon.png" alt="openRAG" />
      <span v-if="!isSidebarCollapsed">openRAG</span>
      <button class="toggle-button" @click="toggleSidebar">
        <span v-if="isSidebarCollapsed">&gt;</span>
        <span v-else>&lt;</span>
      </button>
    </el-header>
    <div id="knowledgetype-header" v-show="!isSidebarCollapsed">
      知识库配置
    </div>
    <el-main class="knowledge-config" v-show="!isSidebarCollapsed">
      <el-row :gutter="0" class="buttons-group">
        <el-button type="primary" @click="handleTabClick('urls')" :plain="currentTab !== 'urls'"
          class="tab-button">URLs</el-button>
        <el-button type="primary" @click="handleTabClick('files')" :plain="currentTab !== 'files'"
          class="tab-button">Files</el-button>
        <el-button type="primary" @click="handleTabClick('images')" :plain="currentTab !== 'images'"
          class="tab-button">Images</el-button>
      </el-row>
      <div v-show="currentTab === 'urls'" class="tab-content content-section active" id="urls-input">
        <el-input type="textarea" class="urls-textarea" v-model="urlsInput" placeholder="请输入URLs，每行一个"></el-input>
      </div>
      <div v-show="currentTab === 'files'" class="tab-content content-section" id="fileUploader">
        <el-select v-model="selectedFileType" placeholder="选择文件类型">
          <el-option label="文档 (.doc, .docx)" value=".doc,.docx"></el-option>
          <el-option label="PDF (.pdf)" value=".pdf"></el-option>
        </el-select>
        <el-upload :multiple="true" :disabled="!selectedFileType" :accept="selectedFileType" action="#" list-type="text"
          :auto-upload="false" :on-change="handleFileChange" :file-list="fileList">
          <el-button slot="trigger" type="primary">选择文件</el-button>
        </el-upload>
      </div>
      <div v-show="currentTab === 'images'" class="tab-content content-section" id="dropArea">
        <el-upload class="upload-demo" drag action="#" list-type="picture" :auto-upload="false"
          :on-change="handleFileChange" :on-preview="handlePreview" :on-remove="handleRemove"
          :on-success="handleSuccess" :accept="accept" :on-exceed="handleExceed" :file-list="imageList">
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">将图片拖到此处，或<em>点击上传</em></div>
        </el-upload>
      </div>
    </el-main>
    <el-footer class="footer-submit" v-show="!isSidebarCollapsed">
      <el-button type="primary" @click="handleSubmit" class="submit-button">提交</el-button>
    </el-footer>
    <el-table :data="pagedData" class="display-section" id="display-table" v-show="!isSidebarCollapsed"
      :row-style="rowStyle">
      <el-table-column prop="index" label="序号" width="15%"></el-table-column>
      <el-table-column prop="type" label="类型" width="15%"></el-table-column>
      <el-table-column prop="file" label="地址" width="30%">
        <template slot-scope="scope">
          <el-tooltip class="item" effect="dark" :content="scope.row.file" placement="top">
            <div class="cell-ellipsis">
              <span>{{ scope.row.file }}</span>
            </div>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="20%"></el-table-column>
      <el-table-column label="操作" width="15%">
        <template slot-scope="scope">
          <el-button size="mini" @click="handleRemoveRow(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
      <el-table-column label="应用" width="15%">
        <template slot-scope="scope">
          <el-switch v-model="scope.row.applied" @change="handleApply(scope.$index, scope.row)"></el-switch>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination background layout="prev, pager, next" :total="submissionList.length" :page-size="pageSize"
      @current-change="handlePageChange" v-show="!isSidebarCollapsed">
    </el-pagination>
  </el-container>
</template>

<script>
import axios from 'axios';
import { EventBus } from '../bus';

export default {
  data() {
    return {
      currentTab: 'urls',
      urlsInput: '',
      selectedFileType: '',
      submissionList: [],
      accept: 'image/*',
      fileList: [],
      imageList: [],
      isSidebarCollapsed: false,
      pageSize: 7,
      currentPage: 1,
      username: localStorage.getItem('username') || '',
      uploads: [],
    };
  },
  //
  created() {
    console.log("created");
    this.fetchUploads();
    EventBus.$on('new-file', this.fetchUploads);
  },
  //
  computed: {
    pagedData() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.submissionList.slice(start, end);
    },
  },
  methods: {
    //页面刷新保留
    async fetchUploads() {
      console.log("fetchUploads");
      try {
        if (this.username) {
          const response = await axios.get(`http://127.0.0.1:5000/api/uploads/${this.username}`);
          this.uploads = response.data;
          this.updateSubmissionList();
        }
      } catch (error) {
        console.error('Error fetching uploads:', error);
      }
    },
    //
    //更新submissionList，确保在页面刷新时保留已上传内容
    updateSubmissionList() {
      this.submissionList = [...this.uploads.map(upload => ({
        index: this.submissionList.length + 1,
        type: upload.type,
        file: upload.file_name,
        status: upload.status,
      }))]
    },

    // 其他方法
    rowStyle() {
      return { height: '30px' }; // 自定义行高为 50px
    },

    handleTabClick(tab) {
      this.currentTab = tab;
    },
    handleFileChange(file, fileList) {
      if (this.currentTab === 'images') {
        this.imageList = fileList;
      } else {
        this.fileList = fileList;
      }
    },
    handlePreview(file) {
      console.log(file);
    },
    handleRemove(file, fileList) {
      if (this.currentTab === 'images') {
        this.imageList = fileList;
      } else {
        this.fileList = fileList;
      }
    },
    handleSuccess(response, file, fileList) {
      if (this.currentTab === 'images') {
        this.imageList = fileList;
      } else {
        this.fileList = fileList;
      }
      console.log(response, file, fileList);
    },
    handleExceed(file, fileList) {
      this.$message.warning(`只能选择 ${fileList.length} 个文件`);
    },

    async handleSubmit() {
      const urls = this.urlsInput.split('\n').filter(url => url.trim() !== '');

      // Add URLs to submission list
      urls.forEach(url => {
        this.submissionList.push({ index: this.submissionList.length + 1, type: 'URL', file: url, status: 'Pending' });
      });

      // Add Files to submission list
      this.fileList.forEach(file => {
        this.submissionList.push({ index: this.submissionList.length + 1, type: 'File', file: file.name, status: 'Pending' });
      });

      // Add Images to submission list
      this.imageList.forEach(image => {
        this.submissionList.push({ index: this.submissionList.length + 1, type: 'Image', file: image.name, status: 'Pending' });
      });

      if (urls.length > 0) {
        try {
          const response = await axios.post('http://127.0.0.1:5000/api/urls', { 
            urls: urls, 
            username: this.username
          },{
              headers: {
            'Content-Type': 'application/json'
          } 
        });
          if (response.status === 200) {
            this.submissionList = this.submissionList.map(item => item.type === 'URL' ? { ...item, status: 'Uploaded' } : item);
          }
        } catch (error) {
          console.error('Error uploading URLs:', error);
        }
      }

      // Send Files to the server
      if (Array.isArray(this.fileList) && this.fileList.length > 0) {
        const formData = new FormData();
        formData.append('username', this.username);
        this.fileList.forEach(file => {
          console.log(file.raw)
          formData.append('files', file.raw);
        });

        try {
          const response = await axios.post('http://127.0.0.1:5000/api/files', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            },
          });
          if (response.status === 200) {
            this.submissionList = this.submissionList.map(item => item.type === 'File' ? { ...item, status: 'Uploaded' } : item);
          }
        } catch (error) {
          console.error('Error uploading files:', error);
        }
      }

      // Send Images to the server
      if (Array.isArray(this.imageList) && this.imageList.length > 0) {
        const formData = new FormData();
        formData.append('username', this.username);
        this.imageList.forEach(image => {
          formData.append('images', image.raw);
        });

        try {
          const response = await axios.post('http://127.0.0.1:5000/api/images', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            },
          });
          if (response.status === 200) {
            this.submissionList = this.submissionList.map(item => item.type === 'Image' ? { ...item, status: 'Uploaded' } : item);
          }
        } catch (error) {
          console.error('Error uploading images:', error);
        }
      }
        
      this.urlsInput = '';
      this.fileList = [];
      this.imageList = [];

    },

    async handleRemoveRow(index, row) {
      // rows.splice(index, 1);
      // this.handlePageChange(this.currentPage);
      console.log(row.file)
      try {
        let response;
        response = await axios.delete('http://127.0.0.1:5000/api/remove', { 
          data: { filename: row.file, username: this.username}
        });
        if (response.status === 200) {
          this.submissionList.splice(index, 1);
          this.handlePageChange(this.currentPage);
        }
      } catch (error) {
        console.error(`Error deleting ${row.type.toLowerCase()}:`, error);
      }
    },

    handleApply(index, row) {
      // 处理应用按钮点击事件的逻辑
      console.log('应用按钮点击', index, row);
      // 在这里添加你希望实现的逻辑，例如调用后端接口或更新状态
    },
    
    handlePageChange(page) {
      this.currentPage = page;
    },

    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed;
      this.$emit('toggle-sidebar', this.isSidebarCollapsed);
    }
  }
}
</script>

<style scoped>
.main-sidebar {
  overflow: hidden;
}

.main-sidebar.collapsed {
  width: 40px;
}

.header {
  display: flex;
  align-items: center;
  text-align: center;
  margin: 0;
}

.header img {
  width: 40px;
  height: 40px;
  vertical-align: middle;
}

.header span {
  font-family: Arial;
  font-size: 30px;
  font-weight: bold;
  text-align: left;
  margin-left: 10px;
}

.toggle-button {
  position: absolute;
  top: 10px;
  right: 0;
  padding: 13px 10px;
  background-color: rgba(255, 255, 255, 0);
  color: rgba(0, 0, 0, 0.5);
  cursor: pointer;
  border: none;
  font-size: 16px;
  transition: all 0.3s;
}

.knowledge-config {
  width: 95%;
  height: 200px;
  border: 3px double rgba(135, 206, 250, 0.5);
  outline: 3px double rgba(173, 216, 230, 0.5);
  padding: 10px;
  border-radius: 10px;
  background-color: rgba(255, 255, 255, 0.8);
  box-sizing: border-box;
  margin: 10px auto;
  flex-grow: 1;
  overflow: auto;
  position: relative;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease height 0.3s ease;
}

.knowledge-config::-webkit-scrollbar {
  width: 8px;
}

.knowledge-config::-webkit-scrollbar-thumb {
  background-color: rgba(135, 206, 250, 0.5);
  border-radius: 4px;
}

.knowledge-config::-webkit-scrollbar-track {
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 4px;
}

#knowledgetype-header {
  font-size: 18px;
  color: #333;
  margin: 10px 10px;
  padding: 10px;
  border: 2px double #b3d9ff;
  background-color: rgba(235, 245, 255, 0.5);
  border-radius: 4px;
  text-align: center;
}

.buttons-group {
  display: flex;
  width: 100%;
}

.buttons-group>>>.el-button {
  flex: 1;
  border: 3px double rgba(135, 206, 250, 0.5);
  padding: 10px;
  border-radius: 10px;
}

.buttons-group>>>.el-button:hover {
  flex: 1;
  background-color: rgba(94, 192, 246, 0.933);
  border: 3px double rgba(135, 206, 250, 0.5);
  padding: 10px;
  border-radius: 10px;
}

.buttons-group>>>.el-button.el-button--primary:focus {
  background-color: #409EFF;
}

.content-section {
  flex: 1;
  margin: 10px 0;
}

.urls-textarea>>>.el-textarea__inner {
  height: 110px;
}

.el-select {
  width: 100%;
}

#fileUploader>>>.el-upload.el-upload--text {
  margin-top: 10px;
}

#dropArea>>>.el-upload.el-upload--picture {
  width: 100%;
}

#dropArea>>>.el-upload-dragger {
  width: 100%;
  height: 110px;
}

#dropArea>>>.el-icon-upload {
  margin: 10px auto;
}

.footer-submit>>>.el-button {
  border: 3px double rgba(135, 206, 250, 0.5);
}

#display-table ::v-deep .el-table__header,
#display-table ::v-deep .el-table__empty-block {
  width: 100% !important;
}

#display-table ::v-deep .el-table__body {
  width: 100% !important;
  /* height: 100%; */
}

#display-table>>>.el-table__cell {
  text-align: center;
  padding: 0 0;
}


#display-table ::v-deep .el-table__body-wrapper {
  height: 210px;
}

.el-pagination {
  text-align: center;
  margin-top: 5px;
}

.file-status {
  margin-top: 10px;
  display: flex;
  align-items: center;
}

.file-status span {
  margin-right: 10px;
}

.file-tag {
  margin: 2px 5px;
}

#display-table .el-table__cell {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cell-ellipsis {
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}
</style>
