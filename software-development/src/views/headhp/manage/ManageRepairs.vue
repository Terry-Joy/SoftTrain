<template>
  <div>
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
        { text: "报修单号", value: "repair_ID" },
        { text: "报修物品", value: "repair_item" },
        { text: "报修宿舍的楼栋", value: "report_from_B_name" },
        { text: "报修宿舍号", value: "report_from_D_number" },
        { text: "学生姓名", value: "report_S_name" },
        { text: "学生联系电话", value: "report_phone_number" },
        { text: "报修时间", value: "report_time" },
        { text: "是否同意", value: "option_s" },
      ],
    };
  },
  methods: {
    submit() {
      for (var i = 0; i < this.desserts.length; i++) {
        if (this.desserts[i].option_s != undefined) {
          console.log(this.desserts[i].repair_ID);
          console.log(this.desserts[i].option_s);
          axios
            .get(
              "http://localhost:8080/api/deal_dormitory_service/deal_repair",
              {
                params: {
                  repair_ID: this.desserts[i].repair_ID,
                  repair_status: this.desserts[i].option_s,
                },
              }
            )
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
        .get("http://localhost:8080/api/deal_dormitory_service/get_repair", {
          params: {},
        })
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