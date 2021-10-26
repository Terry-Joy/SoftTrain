<template>
    <v-container>
    <v-simple-table style="align='center">
      <template v-slot:default>
        <thead>
          <tr>
            <th class="text-left">学号</th>
            <th class="text-left">姓名</th>
            <th class="text-left">性别</th>
            <th class="text-left">学院</th>
            <th class="text-left">年级</th>
            <th class="text-left">班级</th>
            <th class="text-left">联系方式</th>
            <th class="text-left">住宿状态</th>
          </tr>
        </thead>
        <tbody>
          <tr :key="desserts.s_id">
            <td>{{ desserts.s_id }}</td>
            <td>{{ desserts.sname }}</td>
            <td>{{ desserts.sex }}</td>
            <td>{{ desserts.school }}</td>
            <td>{{ desserts.grade }}</td>
            <td>{{ desserts.now_class }}</td>
            <td>{{ desserts.phone_number }}</td>
            <td>{{ dorm }}</td>
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
      dorm:"",
      desserts: "",
    };
  },
  mounted() {
    axios({
      method: "get",
      url: "http://localhost:8080/api/user/get_current_user",
    }).then((res) => {
      this.$data.desserts = res.data;
      if(res.data.live_status=="yes")
      {
        this.$data.dorm=res.data.bel_b_name+"-"+res.data.bel_d_number;
      }
      else
      {
        this.$data.dorm="未住宿";
      }
    });
  },
};
</script>