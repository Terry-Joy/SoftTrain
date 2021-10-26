<template>
  <v-container>
    <v-simple-table style="align='center">
      <template v-slot:default>
        <thead>
          <tr>
            <th class="text-left">工号</th>
            <th class="text-left">姓名</th>
            <th class="text-left">性别</th>
            <th class="text-left">管理楼栋</th>
          </tr>
        </thead>
        <tbody>
          <tr :key="desserts.dorm_administrator_id">
            <td>{{ desserts.dorm_administrator_id }}</td>
            <td>{{ desserts.d_ad_name }}</td>
            <td>{{ desserts.sex }}</td>
            <td>{{ desserts.bel_b_id }}</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </v-container>
</template>
<script>
import axios from "axios";
export default {
  data() {
    return {
      desserts: "",
    };
  },
  mounted() {
    axios({
      method: "get",
      url: "http://localhost:8080/api/user/get_current_user",
    }).then((res) => {
      this.$data.desserts = res.data;
    });
  },
};
</script>
