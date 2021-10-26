<template>
  <v-data-table
    :headers="headers"
    :items="desserts"
    sort-by="id"
    class="elevation-1"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title>学生信息</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialog" max-width="500px">
          <v-card>
            <v-card-title>
              <span class="text-h5">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.s_id"
                      readonly
                      label="学号"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.sname"
                      label="姓名"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.school"
                      label="学院"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.sex"
                      :items="option_sex"
                      readonly
                      label="性别"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.grade"
                      readonly
                      label="年级"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-select
                      v-model="editedItem.now_class"
                      :items="option_class"
                      label="班级"
                    ></v-select>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.phone_number"
                      label="手机号"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.bel_b_name"
                      label="宿舍楼栋"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.bel_d_number"
                      label="宿舍号"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close"> 取消 </v-btn>
              <v-btn color="blue darken-1" text @click="save" :disabled="unable()"> 保存 </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <!-- <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title class="text-h5">确认删除此条数据？</v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeDelete"
                >取消</v-btn
              >
              <v-btn color="blue darken-1" text @click="deleteItemConfirm"
                >确认</v-btn
              >
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog> -->
      </v-toolbar>
    </template>
    <template v-slot:[`item.actions`]="{ item }">
      <v-icon small text class="mr-2" @click="editItem(item)"> 编辑 </v-icon>
      <!-- <v-icon small text @click="deleteItem(item)"> 删除 </v-icon> -->
    </template>
  </v-data-table>
</template>

<script>
import axios from "axios";
export default {
  data: () => ({
    dialog: false,
    dialogDelete: false,
    headers: [
      {
        text: "学号",
        align: "start",
        value: "s_id",
      },
      { text: "姓名", value: "sname", sortable: false },
      { text: "学院", value: "school", sortable: false},
      { text: "性别", value: "sex", sortable: false },
      { text: "年级", value: "grade" },
      { text: "班级", value: "now_class" },
      { text: "手机号", value: "phone_number", sortable: false },
      { text: "宿舍楼栋", value: "bel_b_name"},
      { text: "宿舍号", value: "bel_d_number" },
      { text: "操作", value: "actions", sortable: false },
    ],
    option_sex: ["男", "女"],
    option_class: [1, 2, 3, 4, 5, 6],
    desserts: [],
    editedIndex: -1,
    editedItem: {
      s_id: "",
      school: "",
      sname: "",
      sex: "",
      grade: "",
      now_class: "",
      phone_number: "",
      bel_b_name: "",
      bel_d_number: "",
    },
    defaultItem: {
      s_id: "",
      school: "",
      sname: "",
      sex: "",
      grade: "",
      now_class: "",
      phone_number: "",
      bel_b_name: "",
      bel_d_number: "",
    },
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "新增学生" : "编辑学生信息";
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      let params = {
        s_id: this.s_id,
        school: this.school,
        sname: this.sname,
        sex: this.sex,
        grade: this.grade,
        now_class: this.now_class,
      };
      for (const key in params) if (params[key] == "") delete params[key];
      axios
        .get("http://localhost:8080/api/user/dorm_get_student_information", {
          params: params,
        })
        .then((res) => {
          this.$data.desserts = res.data;
          // console.log(res);
        });
    },

    unable(){
      if(this.editedItem.s_id==""||
      this.editedItem.sname==""||
      this.editedItem.sex==""||
      this.editedItem.school==""||
      this.editedItem.grade==""||
      this.editedItem.now_class=="")
        return true;
      return false;
    },

    editItem(item) {
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    // deleteItem(item) {
    //   this.editedIndex = this.desserts.indexOf(item);
    //   this.editedItem = Object.assign({}, item);
    //   this.dialogDelete = true;
    // },

    // deleteItemConfirm() {
    //   let params = {
    //     s_id: this.editedItem.s_id,
    //     sname: this.editedItem.sname,
    //     school: this.editedItem.school,
    //     sex: this.editedItem.sex,
    //     grade: this.editedItem.grade,
    //     now_class: this.editedItem.now_class,
    //     phone_number: this.editedItem.phone_number,
    //     bel_b_name: this.editedItem.bel_b_name,
    //     bel_d_number: this.editedItem.bel_d_number
    //   };
    //   axios({
    //     method: "get",
    //     url: "",
    //     params: params,
    //   });
    //   this.desserts.splice(this.editedIndex, 1);
    //   this.closeDelete();
    // },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    save() {
      let params = {
        s_id: this.editedItem.s_id,
        sname: this.editedItem.sname,
        school: this.editedItem.school,
        sex: this.editedItem.sex,
        grade: this.editedItem.grade,
        now_class: this.editedItem.now_class,
        phone_number: this.editedItem.phone_number,
        bel_b_name: this.editedItem.bel_b_name,
        bel_d_number: this.editedItem.bel_d_number
      };
      if (this.editedIndex > -1) {
        Object.assign(this.desserts[this.editedIndex], this.editedItem);
        axios({
          method: "get",
          url: "http://localhost:8080/api/system_administrator/update_student",
          params: params,
        });
      } else {
        this.desserts.push(this.editedItem);
      }
      this.close();
    },
  },
};
</script>