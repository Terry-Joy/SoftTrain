<template>
  <div>
    <v-container>
      <v-row justify="center">
        <v-alert type="error" v-if="!authorization">您尚未入住学生宿舍</v-alert>
      </v-row>
      <v-btn color="primary" @click="submitA(), (pay_btn = false)" :disabled="!authorization"
        >未缴费信息</v-btn
      >
      <v-btn color="primary" @click="submitB(), (pay_btn = true)" :disabled="!authorization"
        >缴费历史</v-btn
      >
      <template>
        <v-data-table
          :headers="headers"
          :items="desserts"
          :items-per-page="5"
          class="elevation-1"
          v-model="selected"
          :single-select="singleSelect"
          item-key="repair_ID"
          show-select
          :disable-pagination="!authorization"
          :disable-sort="!authorization"
        ></v-data-table>
      </template>

      <p>&nbsp;</p>
      <v-row>
        <v-col cols="12" md="1" offset="11">
          <v-dialog transition="dialog-bottom-transition" max-width="600">
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                color="primary"
                v-bind="attrs"
                v-on="on"
                :disabled="pay_btn||!authorization"
                >缴费</v-btn
              >
            </template>
            <template v-slot:default="dialog">
              <v-card>
                <v-img
                  class="white--text align-end"
                  height="700px"
                  src="~@/assets/zfb.jpg"
                  alt=""
                >
                </v-img>
                <v-card-actions class="justify-end">
                  <v-btn
                    text
                    color="green"
                    @click="(dialog.value = false), submitC(), refresh()"
                    >支付成功</v-btn
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
      selected: [],
      pay_btn: false,
      headers: [
        { text: "缴费单号", value: "WE_ID" },
        { text: "用水量", value: "W_amount" },
        { text: "用电量", value: "E_amount" },
        { text: "宿舍楼栋", value: "bel_b_name" },
        { text: "宿舍号", value: "bel_d_number" },
        { text: "费用总计", value: "money" },
        { text: "缴费人ID", value: "paid_from_S_ID" },
        { text: "缴费状态", value: "paid_status" },
        { text: "缴费时间", value: "paid_time" },
      ],
      desserts: [],
      authorization: true,
    };
  },
  methods: {
    submitA() {
      axios({
        method: "get",
        url: "http://localhost:8080/api/dormitory_service/get_we_information",
      }).then((res) => {
        this.desserts = res.data;
        console.log(res.data);
      });
    },
    submitB() {
      axios({
        method: "get",
        url: "http://localhost:8080/api/dormitory_service/get_all_we_information",
      }).then((res) => {
        this.desserts = res.data;
        console.log(res.data);
      });
    },
    submitC() {
      console.log(this.$data.selected);
      var list_ID = [];
      for (var i of this.$data.selected) {
        list_ID.push(i);
      }
      for (var j = 0; j < list_ID.length; j++) {
        console.log(list_ID[j].WE_ID);
        axios
          .get("http://localhost:8080/api/dormitory_service/pay_we", {
            params: {
              we_id: String(list_ID[j].WE_ID),
            },
          })
          .then((res) => {
            // this.$data.desserts = res.data;
            console.log(res);
          });
      }
    },

    //更新数据
    refresh() {
      axios
        .get(
          "http://localhost:8080/api/dormitory_service/get_all_we_information",
          {
            params: {},
          }
        )
        .then((res) => {
          this.$data.desserts = res.data;
          console.log(this.$data.desserts);
        },
        (err) => {
            console.log(err.response.data);
            console.log(err.response.status);
            if (err.response.status == 400||err.response.status == 401) {
              this.$data.authorization = false;
            }
          }
        );
    },
  },
  mounted() {
    this.refresh();
  },
};
</script>