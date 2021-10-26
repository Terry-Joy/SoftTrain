<template>
  <div>
    <v-container>
      <template>
        <v-data-table
          :headers="headers"
          :items="desserts"
          :items-per-page="5"
          class="elevation-1"
          v-model="selected"
          :single-select="singleSelect"
          item-key="m_id"
          show-select
        ></v-data-table>
      </template>

      <p>&ensp;</p>
      <v-row>
        <v-col cols="12" md="1" offset="11">
          <v-dialog transition="dialog-bottom-transition" max-width="600">
            <template v-slot:activator="{ on, attrs }">
              <v-btn color="primary" v-bind="attrs" v-on="on" @click="submit"
                >一键分配</v-btn
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
                    @click="(dialog.value = false), (msg = ''), refresh()"
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
      singleSelect: false,
      dialog: false,
      msg: "",
      selected: [],
      headers: [
        { text: "表单号", value: "m_id" },
        { text: "学号", value: "s_id" },
        { text: "姓名", value: "sname" },
        { text: "申请原因", value: "content" },
        { text: "申请时间", value: "move_in_time" },
      ],
      desserts: [],
    };
  },
  methods: {
    submit() {
      var list_ID = [];
      for (var i of this.$data.selected) {
        list_ID.push(i);
      }
      console.log(list_ID);
      for (i = 0; i < list_ID.length; i++) {
        axios
          .get("http://localhost:8080/api/move_in/accecp_for_move_in", {
            params: {
              m_id: list_ID[i].m_id,
            },
          })
          .then((res) => {
            console.log(res);
            if (res.status == 200) {
              console.log(res.data);
              this.msg = "提交成功";
            } else {
              this.msg = "提交失败";
            }
          });
      }
    },
    // cleardesserts() {
    //   var list = new Object();
    //   list.m_id = "";
    //   list.s_id = "";
    //   this.desserts = list;
    // },
    //更新数据
    refresh() {
      axios
        .get("http://localhost:8080/api/move_in/get_information", {
          params: {},
        })
        .then((res) => {
          this.$data.desserts = res.data;
          console.log(this.$data.desserts);
        });
    },
  },
  mounted() {
    this.refresh();
  },
};
</script>