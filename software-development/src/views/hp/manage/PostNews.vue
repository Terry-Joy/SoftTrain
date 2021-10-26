<template>
  <div class="text-center">
    <p>&ensp;</p>
    <v-container>
      <v-form>
        <v-row>
          <v-col cols="12" md="3">
            <v-text-field
              v-model="N_title"
              label="公告标题(60字以内)"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="9">
            <v-textarea
              outlined
              label="公告内容(60字以内)"
              auto-grow
              v-model="content"
            >
            </v-textarea>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="1" offset="8">
            <v-dialog transition="dialog-bottom-transition" max-width="500">
              <template v-slot:activator="{ on, attrs }">
                <v-btn color="primary" @click="submit" v-bind="attrs" v-on="on"
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
                          ((content = ''), (N_title = ''), (msg = ' '))
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
      </v-form>
    </v-container>
  </div>
</template>

<script lang="ts">
import axios from "axios";
import Vue from "vue";
export default Vue.extend({
  data: () => {
    return {
      N_title: "",
      content: "",
      msg: " ",
      dialog: false,
    };
  },
  methods: {
    submit() {
      //提交不能为空
      if (this.N_title == "" && this.content == "") {
        this.msg = "提交内容不能为空";
        return;
      }
      this.N_title = String(this.N_title);
      this.content = String(this.content);
      //请求
      axios
        .get("http://localhost:8080/api/deal_dormitory_service/send_notice", {
          params: {
            N_title: this.N_title,
            content: this.content,
          },
        })
        .then((res) => {
          if (res.status == 200) {
            this.msg = "提交成功";
          } else {
            this.msg = "提交失败";
          }
          console.log(res.data);
          console.log(this.msg);
        })
        .catch();
    },
  },
});
</script>