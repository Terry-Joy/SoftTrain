<template>
  <v-app>
    <nav>
      <v-app-bar app color="primary">
        <v-app-bar-nav-icon
          @click="drawer = !drawer"
          style="color: white"
        ></v-app-bar-nav-icon>
        <v-app-bar-title class="text-uppercase">
          <span class="mr-2" style="color: white">宿舍管理系统</span>
        </v-app-bar-title>

        <v-spacer></v-spacer>
        <v-btn @click="backhome()" text>
          <span class="mr-2" style="color: white">首页</span>
          <v-icon style="color: white">mdi-home</v-icon>
        </v-btn>

        <v-btn @click="logout()" text>
          <span class="mr-2" style="color: white">退出登录</span>
          <v-icon style="color: white">mdi-open-in-new</v-icon>
        </v-btn>

        <div class="text-center">
          <v-dialog v-model="dialog" width="500">
            <template v-slot:activator="{ on, attrs }">
              <v-btn color="red lighten-2" dark v-bind="attrs" v-on="on">
                修改密码
              </v-btn>
            </template>
            <v-card>
              <v-card-title class="text-h5 grey lighten-2">
                输入需要修改的密码
              </v-card-title>

              <v-card-text>
                <v-text-field v-model="pw"></v-text-field>
              </v-card-text>

              <v-divider></v-divider>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" text @click="dialog = false">
                  取消
                </v-btn>
                <template>
                  <div class="text-center ma-2">
                    <v-btn dark @click="(snackbar = true), modifyPW()">
                      确认
                    </v-btn>
                    <v-snackbar v-model="snackbar" top timeout="-1">
                      {{ msg }}

                      <template v-slot:action="{ attrs }">
                        <v-btn
                          color="pink"
                          text
                          v-bind="attrs"
                          @click="
                            (snackbar = false), $router.push({ path: '/login' })
                          "
                        >
                          确认
                        </v-btn>
                      </template>
                    </v-snackbar>
                  </div>
                </template></v-card-actions
              ></v-card
            ></v-dialog
          >
        </div>
      </v-app-bar>

      <v-navigation-drawer app v-model="drawer">
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="text-h6">菜单</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>

        <v-list>
          <template v-for="list in navList">
            <v-list-group
              :value="true"
              class="white--text"
              :key="list.path"
              no-action
              sub-group
            >
              <template v-slot:activator>
                <v-list-item-content>
                  <v-list-item-title v-text="list.title"></v-list-item-title>
                </v-list-item-content>
              </template>

              <v-list-item
                v-for="item in list.items"
                :key="item.title"
                :to="item.path"
              >
                <v-list-item-action
                  ><v-icon v-text="item.icon"></v-icon
                ></v-list-item-action>
                <v-list-item-content>
                  <v-list-item-title v-text="item.title"></v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-group>
          </template>
        </v-list>
      </v-navigation-drawer>
    </nav>
    <v-content><span>&nbsp;</span><router-view /></v-content>
  </v-app>
</template>

<script>
import axios from "axios";
export default {
  name: "Navigation",
  props: {
    miniNav: Boolean,
    backgroundNav: Boolean,
  },
  data() {
    return {
      drawer: false,
      dialog: false,
      snackbar: false,
      pw: "",
      msg: "",
      navList: [
        {
          title: "查询信息",
          icon: "mdi-lightbulb-outline",
          group: "/hp",
          items: [
            {
              title: "查询学生信息",
              path: "/hp/querystu",
              icon: "mdi-transition-masked",
            },
            {
              title: "查询个人信息",
              path: "/hp/queryself",
              icon: "mdi-transition-masked",
            },
            {
              title: "查看公告",
              path: "/hp/querynews",
              icon: "mdi-transition-masked",
            },
          ],
        },
        {
          title: "管理信息",
          icon: "mdi-lightbulb-outline",
          group: "/hp",
          items: [
            {
              title: "处理离校申请",
              path: "/hp/manageout",
              icon: "mdi-transition-masked",
            },
            {
              title: "处理报修申请",
              path: "/hp/managerepairs",
              icon: "mdi-transition-masked",
            },
            {
              title: "发布公告",
              path: "/hp/postnews",
              icon: "mdi-transition-masked",
            },
          ],
        },
      ],
    };
  },
  methods: {
    modifyPW() {
      axios
        .get("http://localhost:8080/api/user/update_user_password", {
          params: {
            password: String(this.pw),
          },
        })
        .then((res) => {
          this.$data.desserts = res.data;
          if (
            res.data.msg == "password update successfully, please login again"
          ) {
            console.log(123);
            this.msg = "密码修改成功，请重新登录";
          }
        });
    },
    logout() {
      localStorage.removeItem("token");
      axios({
        method: "get",
        url: "http://localhost:8080/api/user/logout",
      }).then((res) => {
        console.log(res.data.msg);
      });
      this.$router.push("/login");
    },
    backhome() {
      this.$router.push("/hphome");
    },
  },
};
</script>