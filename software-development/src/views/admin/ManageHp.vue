<template>
  <v-data-table
    :headers="headers"
    :items="desserts"
    sort-by="id"
    class="elevation-1"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title>宿管信息</v-toolbar-title>
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
                      v-model="editedItem.dorm_administrator_id"
                      readonly
                      label="工号"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.d_ad_name"
                      label="姓名"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.sex"
                      readonly
                      :items="option_sex"
                      label="性别"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.bel_b_id"
                      label="管理楼栋"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close()"> 取消 </v-btn>
              <v-btn
                color="blue darken-1"
                text
                @click="save()"
                :disabled="unable()"
              >
                保存
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <!-- <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title class="text-h5">确认删除此条数据？</v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeDelete">取消</v-btn>
              <v-btn color="blue darken-1" text @click="deleteItemConfirm">确认</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog> -->
      </v-toolbar>
    </template>
    <template v-slot:[`item.actions`]="{ item }">
      <v-icon small text class="mr-2" @click="editItem(item)"> 编辑 </v-icon>
      <!-- <v-icon
        small
        text
        @click="deleteItem(item)"
      >
        删除
      </v-icon> -->
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
        text: "工号",
        align: "start",
        value: "dorm_administrator_id",
      },
      { text: "姓名", value: "d_ad_name", sortable: false },
      { text: "性别", value: "sex", sortable: false },
      { text: "管理楼栋", value: "bel_b_id" },
      { text: "操作", value: "actions", sortable: false },
    ],
    option_sex: ["男", "女"],
    desserts: [],
    editedIndex: -1,
    editedItem: {
      dorm_administrator_id: "",
      d_ad_name: "",
      sex: "",
      bel_b_id: "",
    },
    defaultItem: {
      dorm_administrator_id: "",
      d_ad_name: "",
      sex: "",
      bel_b_id: "",
    },
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "新增宿管" : "编辑宿管信息";
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
        dorm_administrator_id: this.dorm_administrator_id,
        d_ad_name: this.d_ad_name,
        bel_b_id: this.bel_b_id,
      };
      for (const key in params) if (params[key] == "") delete params[key];
      axios
        .get("http://localhost:8080/api/system_administrator/get_all_dorm", {
          params: params,
        })
        .then((res) => {
          this.$data.desserts = res.data;
          // console.log(res);
        });
    },

    unable() {
      if (
        this.editedItem.h_id == "" ||
        this.editedItem.hname == "" ||
        this.editedItem.sex == "" ||
        this.editedItem.bel_b_id == ""
      )
        return true;
      return false;
    },

    editItem(item) {
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    // deleteItem (item) {
    //   this.editedIndex = this.desserts.indexOf(item)
    //   this.editedItem = Object.assign({}, item)
    //   this.dialogDelete = true
    // },

    // deleteItemConfirm () {
    //   this.desserts.splice(this.editedIndex, 1)
    //   this.closeDelete()
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
        dorm_administrator_id: this.editedItem.dorm_administrator_id,
        d_ad_name: this.editedItem.d_ad_name,
        sex: this.editedItem.sex,
        bel_b_id: this.editedItem.bel_b_id,
      };
      if (this.editedIndex > -1) {
        Object.assign(this.desserts[this.editedIndex], this.editedItem);
        axios({
          method: "get",
          url: "http://localhost:8080/api/system_administrator/update_dorm",
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