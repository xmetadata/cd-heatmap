<template>
  <div class="app-container">
    <div
      v-for="manual in tableData"
      :key="manual.uuid"
      style="margin: 10px; white-space: pre-line; line-height: 26px;"
    >
      <el-card>
        <div slot="header">
          <span>{{ manual.title }}</span>
        </div>
        <div>
          <span>{{ manual.content }}</span>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import {
  getList,
  getDetail,
  getData,
  create,
  update,
  remove
} from "@/api/manuals";

export default {
  data() {
    return {
      listLoading: true,
      tableData: []
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      this.listLoading = true;
      getList(this.listQuery).then(response => {
        this.tableData = response;
        this.listLoading = false;
      });
    }
  }
};
</script>
