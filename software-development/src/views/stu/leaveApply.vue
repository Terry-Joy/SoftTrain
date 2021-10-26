
<template>
  <v-form id="leaveInfo">
    <!-- 离校原因下拉框 -->
    <v-row justify="center">
      <v-alert type="error" v-if="!authorization">您尚未入住学生宿舍</v-alert>
    </v-row>
    <v-row justify="center">
      <v-col cols="12" md="4">
        <v-select
          v-model="select"
          :items="items"
          label="离校原因"
          :disabled="!authorization"
        ></v-select>
      </v-col>
    </v-row>
    <!-- 其他原因填写 -->
    <v-row justify="center">
      <v-col cols="12" md="4">
        <v-text-field
          v-if="select == '其他'"
          label="其他原因填写(60字以内)"
          v-model="otherReason"
        >
        </v-text-field>
      </v-col>
    </v-row>
    <!-- 离校时间选择 -->
    <v-row justify="center">
      <v-col cols="12" md="4">
        <v-dialog
          ref="dialog"
          v-model="modal"
          :return-value.sync="leaveDate"
          width="290px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="leaveDate"
              label="离校时间"
              readonly
              v-bind="attrs"
              v-on="on"
              :disabled="!authorization"
            ></v-text-field>
          </template>
          <v-date-picker :min="curDate()" v-model="leaveDate" scrollable>
            <v-spacer></v-spacer>
            <v-btn text color="primary" @click="modal = false"> 取消 </v-btn>
            <v-btn text color="primary" @click="$refs.dialog.save(leaveDate)">
              确认
            </v-btn>
          </v-date-picker>
        </v-dialog>
      </v-col>
    </v-row>
    <!-- 按钮 -->
    <v-row justify="center">
      <v-col>&nbsp;</v-col>
      <v-col col="12" md="4">
        <v-dialog transition="dialog-bottom-transition" max-width="600">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              color="primary"
              v-bind="attrs"
              v-on="on"
              :disabled="displayBTN()"
              @click="submit()"
              >提交申请</v-btn
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
                  @click="(dialog.value = false), (leaveDate = ''), (select = ''), (otherReason = ''), refresh()">关闭</v-btn
                >
              </v-card-actions>
            </v-card>
          </template>
        </v-dialog>
      </v-col>
    </v-row>
    <v-row><v-col></v-col></v-row>
    <v-row>
      <v-col>
        <v-container>
          <v-simple-table style="align='center">
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">学号</th>
                  <th class="text-left">姓名</th>
                  <th class="text-left">离校原因</th>
                  <th class="text-left">离校日期</th>
                  <th class="text-left">申请状态</th>
                </tr>
              </thead>
              <tbody>
                <tr :key="s_ID">
                  <td>{{ s_ID }}</td>
                  <td>{{ s_name }}</td>
                  <td>{{ appliedReason }}</td>
                  <td>{{ leave_date }}</td>
                  <td>
                    {{ serve_status }}
                    &nbsp;&nbsp;
                    <v-dialog
                      transition="dialog-bottom-transition"
                      max-width="600"
                    >
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          color="primary"
                          v-bind="attrs"
                          v-on="on"
                          v-if="displayCancelBTN"
                          @click="cancelApply()"
                          >撤销申请</v-btn>
                      </template>
                      <template v-slot:default="dialog">
                        <v-card>
                          <v-toolbar color="primary" dark>提示</v-toolbar>
                          <v-card-text>
                            <div class="text-h2 pa-12">{{ cancelMsg }}</div>
                          </v-card-text>
                          <v-card-actions class="justify-end">
                            <v-btn text color="green" @click="(dialog.value = false), refresh()">关闭</v-btn>
                          </v-card-actions>
                        </v-card>
                      </template>
                    </v-dialog>
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-container>
      </v-col>
    </v-row>
  </v-form>
</template>

<script>
import axios from "axios";
import Vue from "vue";
export default {
  data: () => ({
    select: "",
    items: ["毕业", "请假", "其他"],
    otherReason: "",
    leaveDate: "",
    menu: false,
    modal: false,
    menu2: false,
    appliedReason: "",
    s_ID: "",
    s_name: "",
    leave_date: "",
    serve_status: "",
    displayCancelBTN: false,
    authorization: true,
    msg: "",
    cancelMsg: "",
  }),
  methods: {
    refresh() {
      axios({
        method: "get",
        url: "http://localhost:8080/api/leave_school/stu_get_leave_school_information",
      }).then(
        (res) => {
          if (res.data == null) {
            this.s_ID = "";
            this.s_name = "";
            this.leave_date = "";
            this.serve_status = "";
            this.appliedReason = "";
            this.displayCancelBTN = false;
          } else {
            this.s_ID = res.data.leave_S_ID;
            this.s_name = res.data.leave_S_name;
            this.leave_date = res.data.leave_date;
            this.serve_status = res.data.serve_status;
            this.displayCancelBTN = true;
            if (res.data.leave_kind == "其他") {
              this.$data.appliedReason = res.data.leave_reason;
            } else {
              this.$data.appliedReason = res.data.leave_kind;
            }
          }
        },
        (err) => {
          console.log(err.response.data);
          console.log(err.response.status);
          if (err.response.status == 400 || err.response.status == 401) {
            this.$data.authorization = false;
          }
        }
      );
    },

    displayBTN() {
      if (
        (this.$data.select == "毕业" || this.$data.select == "请假") &&
        this.$data.leaveDate != ""
      ) {
        return false;
      }

      if (
        this.$data.select == "其他" &&
        this.$data.otherReason != "" &&
        this.$data.leaveDate != ""
      ) {
        return false;
      }

      return true;
    },

    submit() {
      var leave_kind = this.$data.select;
      var leave_reason = this.$data.otherReason;
      var leave_date = this.$data.leaveDate;
      axios({
        method: "get",
        url: "http://localhost:8080/api/leave_school/apply_for_leave_school",
        params: {
          leave_kind: leave_kind,
          leave_reason: leave_reason,
          leave_date: leave_date,
        },
      }).then((res) => {
        this.$data.desserts = res.data;
        console.log(res.data);
        if (res.data.message == "OK: sumbit successfully.") {
          this.msg = "提交成功";
        } else {
          this.msg = "提交失败";
        }
        console.log(this.$data.msg);
      });
    },

    cancelApply() {
      axios({
        method: "get",
        url: "http://localhost:8080/api/leave_school/cancel",
      }).then((res) => {
        console.log(res.data);
        if (res.status == 200) {
          console.log(res.data);
          this.cancelMsg = "撤销成功";
        } else {
          this.cancelMsg = "撤销失败";
        }

      });
    },

    curDate() {
      var curDate = new Date();
      var allowedDates =
        curDate.getFullYear() +
        "-" +
        (curDate.getMonth() + 1 < 10
          ? "0" + (curDate.getMonth() + 1)
          : curDate.getMonth() + 1) +
        "-" +
        (curDate.getDate() + 1 < 10
          ? "0" + (curDate.getDate() + 1)
          : curDate.getDate() + 1);
      return allowedDates;
    },
  },
  mounted() {
    this.refresh();
  },
};
</script>