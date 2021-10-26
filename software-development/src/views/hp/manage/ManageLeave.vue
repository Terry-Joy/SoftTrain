<template>
  <div>
    <v-container>
      <v-data-table :headers="headers" :items="desserts" class="elevation-1">
        <template v-slot:[`item.option_s`]="{ item }">
          <v-select v-model="item.option_s" :items="options"></v-select>
        </template>
      </v-data-table>
      <p></p>
      <v-row>
        <v-col cols="12" md="1" offset="11">
          <v-dialog transition="dialog-bottom-transition" max-width="500">
            <template v-slot:activator="{ on, attrs }">
              <v-btn color="primary" v-bind="attrs" v-on="on" @click="submit"
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
                    @click="(dialog.value = false), refresh(), (msg = ' ')"
                    >关闭</v-btn
                  >
                </v-card-actions>
              </v-card>
            </template>
          </v-dialog>
        </v-col>
        <v-col>&ensp;</v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
import axios from "axios";
export default {
  data() {
    return {
      msg: " ",
      options: ["同意", "拒绝"],
      desserts: [],
      headers: [
        { text: "学生姓名", value: "leave_S_name" },
        { text: "学号", value: "leave_S_ID" },
        { text: "学生所住楼栋", value: "leave_S_bel_B_name" },
        { text: "宿舍号", value: "leave_S_bel_D_number" },
        { text: "离校日期", value: "leave_date" },
        { text: "离校类型", value: "leave_kind" },
        { text: "其他原因", value: "leave_reason" },
        { text: "是否同意", value: "option_s" },
      ],
    };
  },
  methods: {
    submit() {
      for (var i = 0; i < this.desserts.length; i++) {
        if (this.desserts[i].option_s != undefined) {
          console.log(this.desserts[i].leave_S_ID);
          console.log(this.desserts[i].option_s);
          axios
            .get("http://localhost:8080/api/leave_school/handle_leave_school", {
              params: {
                leave_S_ID: this.desserts[i].leave_S_ID,
                status: this.desserts[i].option_s,
              },
            })
            .then((res) => {
              if (res.status == 200) {
                console.log(res.data);
                this.msg = "提交成功";
              } else {
                this.msg = "提交失败";
              }
            });
        }
      }
    },
    //更新数据
    refresh() {
      axios
        .get(
          "http://localhost:8080/api/leave_school/dorm_get_leave_school_information",
          {
            params: {},
          }
        )
        .then((res) => {
          this.$data.desserts = res.data;
        });
    },
  },
  mounted() {
    this.refresh();
  },
};
</script>