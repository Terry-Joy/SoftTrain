<template>
    <v-app>
        <v-app-bar height="64" color="primary" clipped-left app dark>
            <v-toolbar-title>
                <v-avatar tile>
                    <v-icon size="40" style="transform: rotate(180deg)">mdi-android-auto</v-icon>
                </v-avatar> 宿舍管理系统
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-toolbar-items>
                <v-btn text @click="backhome()">
                    <v-text>回到首页</v-text>
                </v-btn>
            </v-toolbar-items>
            <v-toolbar-items>
                <v-btn text @click="logout()">
                    <v-text>退出登录</v-text>
                </v-btn>
            </v-toolbar-items>
        </v-app-bar>

        <Navigation :miniNav="miniNav" :backgroundNav="backgroundNav" />
    </v-app>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import Navigation from '../components/headhpNav.vue'

export default {
    name: 'Home',
    components: {
        Navigation
    },
    data() {
        return {
        }
    },
    methods: {
        ...mapActions(['hideSnackbar']),
        logout() {
            localStorage.removeItem('token')
            this.$router.push('/login')
        },
        backhome() {
            this.$router.push('/headhphome')
        }
    },
}
</script>