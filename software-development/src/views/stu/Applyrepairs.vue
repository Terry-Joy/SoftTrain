<template>
  <body>
    <v-form id="f">
      <v-container>
        <v-row justify="center">
        <v-alert type="error" v-if="!authorization">您尚未入住学生宿舍</v-alert>
        </v-row>
        <v-row justify="center">
          <v-col cols="12" md="8">
            <v-text-field v-model="Tel" label="联系电话" :disabled="!authorization"></v-text-field>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
    <v-form>
      <v-container>
        <v-row justify="center">
          <v-col cols="12" md="8">
            <v-textarea outlined label="报修内容" auto-grow v-model="news" :disabled="!authorization">
            </v-textarea>
          </v-col>
        </v-row>
        <v-row>
          <v-col>&ensp;</v-col>
          <v-col>&ensp;</v-col>
          <v-col>&ensp;</v-col>
          <v-col>&ensp;</v-col>
          <v-col cols="12" md="1">
            <v-dialog transition="dialog-bottom-transition" max-width="600">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  color="primary"
                  v-bind="attrs"
                  v-on="on"
                  @click="submit()"
                  :disabled="displayBTN()"
                  >提交</v-btn
                >
              </template>
              <template v-slot:default="dialog">
                <v-card>
                  <v-toolbar color="primary" dark>提示</v-toolbar>
                  <v-card-text>
                    <div class="text-h2 pa-12">{{ msg }}</div>
                  </v-card-text>
                  <v-card-actions class="justify-end">
                    <v-btn
                      text
                      color="green"
                      @click="
                        (dialog.value = false),
                          (Tel = ''),
                          (news = ''),
                          (msg = ' '),
                          refresh()
                      "
                      >关闭</v-btn
                    >
                  </v-card-actions>
                </v-card>
              </template>
            </v-dialog>
          </v-col>
          <v-col>&ensp;</v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <div>
              <v-container>
                <v-data-table
                  :headers="headers"
                  :items="desserts"
                  :items-per-page="5"
                  class="elevation-1"
                  :disable-pagination="!authorization"
                  :disable-sort="!authorization"
                ></v-data-table>
              </v-container>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </body>
</template>

<script>
import axios from "axios";
import Vue from "vue";
export default {
  data: () => ({
    Tel: "",
    news: "",
    msg: " ",
    headers: [
      { text: "报修单号", value: "repair_ID" },
      { text: "报修物品", value: "repair_item" },
      { text: "联系电话", value: "report_phone_number" },
      { text: "报修时间", value: "report_time" },
      { text: "报修状态", value: "repair_status" },
    ],
    desserts: [],
    authorization: true
  }),
  methods: {
    displayBTN() {
      if (this.$data.Tel == "" || this.$data.news == "") return true;
      else return false;
    },

    refresh() {
      axios
        .get("http://localhost:8080/api/dormitory_service/see_repair", {
          params: {},
        })
        .then(
          (res) => {
            this.$data.desserts = res.data;
            console.log(res);
          },
          (err)=>{
            console.log(err.response.data);
            console.log(err.response.status);
            if(err.response.status == 400||err.response.status == 401)
            {
              this.$data.authorization = false;
            }
            
          }
        )
    },

    submit() {
      axios
        .get("http://localhost:8080/api/dormitory_service/create_repair", {
          params: {
            phone_number: String(this.$data.Tel),
            repair_item: String(this.$data.news),
          },
        })
        .then((res) => {
          if (res.status == 200) {
            console.log(res.data);
            this.msg = "提交成功";
          } else {
            this.msg = "提交失败";
          }
          // this.$data.desserts = res.data.message;
          // console.log(this.$data.desserts);
          // this.refresh();
        });
    },
  },
  mounted() {
    this.refresh();
  },
};
</script>