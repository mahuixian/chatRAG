<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <div class="login-container">
        <el-form :model="form" ref="form" label-width="80px" class="login-form">
            <el-form-item label="用户名" prop="username" :rules="rules.username">
                <el-input v-model="form.username" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password" :rules="rules.password">
                <el-input type="password" v-model="form.password" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="handleLogin">登录</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
// import axios from 'axios';
import { api } from '../api'

export default {
    name: 'MainLogin',
    data() {
        return {
            form: {
                username: '',
                password: ''
            },
            rules: {
                username: [
                    { required: true, message: '请输入用户名', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: '请输入密码', trigger: 'blur' }
                ]
            }
        };
    },
    methods: {
        async handleLogin() {
            try {
                // 验证表单
                const valid = await new Promise((resolve) => {
                    this.$refs.form.validate((valid) => {
                        resolve(valid);
                    });
                });

                if (valid) {
                    // 执行登录请求
                    // const response = await axios.post('http://127.0.0.1:5000/api/login', this.form);
                    const response = await api.login(this.form)

                    if (response.data.success) {
                        localStorage.setItem('token', response.data.token); // 设置 token
                        localStorage.setItem('username', this.form.username);
                        this.$router.push({ name: 'Main' });
                    } else {
                        this.$message.error('用户名或密码错误');
                    }
                } else {
                    console.log('error submit!!');
                }
            } catch (error) {
                console.error('Login error:', error);
                this.$message.error('登录失败，请稍后再试');
            }
        }
        // handleLogin() {
        //     this.$refs.form.validate((valid) => {
        //         if (valid) {
        //             axios.post('http://127.0.0.1:5000/api/login', this.form)
        //                 .then(response => {
        //                     if (response.data.success) {
        //                         localStorage.setItem('token', response.data.token); // 设置token
        //                         localStorage.setItem('username', this.form.username);
        //                         this.$router.push({ name: 'Main' });
        //                     } else {
        //                         this.$message.error('用户名或密码错误');
        //                     }
        //                 })
        //                 .catch(error => {
        //                     console.error('Login error:', error);
        //                     this.$message.error('登录失败，请稍后再试');
        //                 });
        //         } else {
        //             console.log('error submit!!');
        //             return false;
        //         }
        //     });
        // }
    }
};
</script>

<style scoped>
.login-container {
    width: 300px;
    margin: 100px auto;
    padding: 40px;
    background: #fff;
    box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
}

.login-form {
    text-align: center;
}
</style>
