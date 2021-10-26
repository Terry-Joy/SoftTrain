<template>
  <body>
    <v-form>
      <v-container>
        <v-row justify="center">
          <v-col cols="12" md="8">
            <v-textarea
              outlined
              label="申请原因(60字以内)"
              auto-grow
              v-model="news"
            ></v-textarea>
          </v-col>
        </v-row>
        <v-row>
          <v-col>&nbsp;</v-col>
          <v-col cols="12" md="3">
            <v-dialog transition="dialog-bottom-transition" max-width="600">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  color="primary"
                  v-bind="attrs"
                  v-on="on"
                  :disabled="displayBTN()"
                  @click="submit()"
                  >申请入住</v-btn
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
                      @click="(dialog.value = false), (news = ''), refresh()"
                      >关闭</v-btn
                    >
                  </v-card-actions>
                </v-card>
              </template>
            </v-dialog>
          </v-col>
        </v-row>
        <v-row>
          <v-container>
            <v-data-table
              :headers="headers"
              :items="desserts"
              :items-per-page="5"
              class="elevation-1"
            ></v-data-table>
          </v-container>
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
    news: "",
    msg: "",
    headers: [
      { text: "表单号", value: "m_id" },
      { text: "学号", value: "s_id" },
      { text: "姓名", value: "sname" },
      { text: "申请原因", value: "content" },
      { text: "分配宿舍名", value: "move_in_b_name" },
      { text: "分配宿舍号", value: "move_in_d_number" },
      { text: "申请时间", value: "move_in_time" },
      { text: "状态", value: "move_in_status" },
    ],
    desserts: [],
  }),
  methods: {
    displayBTN() {
      if (this.$data.news == "") return true;
      else return false;
    },
    refresh() {
      axios({
        method: "get",
        url: "http://localhost:8080/api/move_in/get_move_in_information",
      }).then((res) => {
        this.desserts = res.data;
        console.log(res.data);
      });
    },

    submit() {
      axios({
        method: "get",
        url: "http://localhost:8080/api/move_in/apply_for_move_in",
        params: { content: this.news },
      }).then((res) => {
        console.log(res.data);
        if (res.status == 200) {
          console.log(res.data);
          this.msg = "提交成功";
        } else {
          this.msg = "提交失败";
        }
      });
    },
  },
  mounted() {
    this.refresh();
  },
};
</script>