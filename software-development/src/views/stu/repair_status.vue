<template>
  <div>
    <v-container>
      <v-data-table
        :headers="headers"
        :items="desserts"
        :items-per-page="5"
        class="elevation-1"
      ></v-data-table>
    </v-container>
  </div>
</template>

<script >
import Vue from "vue";
import axios from "axios";
export default {
  data: () => ({
    headers: [
      { text: "报修单号", value: "repair_ID" },
      { text: "报修物品", value: "repair_item" },
      { text: "联系电话", value: "report_phone_number" },
      { text: "报修时间", value: "report_time" },
      { text: "报修状态", value: "repair_status" },
    ],
    desserts: [],
  }),
  mounted() {
    axios
      .get("http://localhost:8080/api/dormitory_service/see_repair", {
        params: {},
      })
      .then((res) => {
        this.$data.desserts = res.data;
        console.log(res);
      });
  },
};
</script>