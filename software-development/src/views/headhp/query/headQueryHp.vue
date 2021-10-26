<template>
  <div>
    <template>
      <!--表单-->
      <v-container>
        <v-form>
          <v-row>
            <v-col cols="12" md="3">
              <v-text-field v-model="h_id" label="工号"></v-text-field>
            </v-col>
            <v-col cols="12" md="3">
              <v-text-field v-model="hname" label="姓名"></v-text-field>
            </v-col>
            <v-col cols="12" md="3">
              <v-text-field v-model="building" label="管理楼栋"></v-text-field>
            </v-col>
            <v-col cols="12" md="1" offset="1">
              <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    color="primary"
                    class="mr-4"
                    @click="submit"
                    v-bind="attrs"
                    v-on="on"
                  >
                    查询
                  </v-btn>
                </template>
                <span>若不选择条件则查看所有宿管</span>
              </v-tooltip>
            </v-col>
          </v-row>
        </v-form>
      </v-container>
    </template>

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

<script>
import axios from "axios";
import Vue from "vue";
export default {
  data: () => ({
    h_id: "",
    hname: "",
    hSex: "",
    hName: "",
    building: "",
    errmsg: "",

    headers: [
      { text: "工号", value: "dorm_administrator_id" },
      { text: "姓名", value: "d_ad_name" },
      { text: "性别", value: "sex" },
      { text: "管理楼栋", value: "bel_b_id" },
    ],
    desserts: [],
  }),
  methods: {
    submit() {
      let params = {
        dorm_administrator_id: this.h_id,
        d_ad_name: this.hname,
        bel_b_id: this.building,
      };
      //若空则在params中删除
      for (const key in params) if (params[key] == "") delete params[key];
      console.log(params);
      axios
        .get("http://localhost:8080/api/system_administrator/get_all_dorm", {
          params: params,
        })
        .then((res) => {
          this.$data.desserts = res.data;
          for (var i = 0; i < this.desserts.length; i++) {
            if (this.desserts[i].bel_b_id == "all")
              this.desserts[i].bel_b_id = "所有楼栋";
          }
          console.log(res);
        });
    },
  },
};
</script>