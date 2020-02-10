<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.title"
        placeholder="板块名称"
        style="width: 260px;"
        class="filter-item"
        @keyup.enter.native="searchData"
      />
      <el-button class="filter-item" type="primary" icon="el-icon-search" @click="searchData">检索</el-button>
      <router-link :to="'/blockset/create'">
        <el-button
          class="filter-item"
          style="margin-left: 10px;"
          type="primary"
          icon="el-icon-plus"
        >添加</el-button>
      </router-link>
    </div>

    <el-table v-loading="listLoading" :data="tableData" style="width: 100%">
      <el-table-column fixed prop="title" label="名称"></el-table-column>
      <el-table-column fixed prop="area" label="面积/k㎡"></el-table-column>
      <el-table-column fixed="right" label="操作">
        <template slot-scope="scope">
          <router-link :to="'/blockset/preview/'+scope.row.uuid">
            <el-button type="success" size="small" icon="el-icon-view" title="板块预览" circle></el-button>
          </router-link>
          <router-link :to="'/blockset/edit/'+scope.row.uuid">
            <el-button type="primary" size="small" icon="el-icon-edit" title="编辑板块" circle></el-button>
          </router-link>
          <el-button
            type="danger"
            size="small"
            icon="el-icon-delete"
            title="删除板块"
            circle
            @click="handleDelete(scope.row)"
          ></el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="pagination">
      <el-pagination
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="listQuery.page"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="10"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      ></el-pagination>
    </div>
  </div>
</template>

<script>
import { getList, getDetail, create, update, remove } from "@/api/blockset";

export default {
  name: "BlocksetList",
  data() {
    return {
      listLoading: true,
      total: 0,
      listQuery: {
        page: 1,
        pre_page: 10,
        title: undefined
      },
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
        this.total = response.total;
        this.tableData = response.items;
        this.listLoading = false;
      });
    },
    resetQuery() {
      this.listQuery = {
        title: "",
        page: 1,
        pre_page: 10
      };
      this.fetchData();
    },
    searchData() {
      this.listQuery.page = 1;
      this.listQuery.pre_page = 20;
      this.fetchData();
    },
    handleSizeChange(val) {
      this.listQuery.pre_page = val;
      this.fetchData();
    },
    handleCurrentChange(val) {
      this.listQuery.page = val;
      this.fetchData();
    },
    handleDelete(row) {
      this.$confirm("此操作将永久删除该记录, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        remove(row.uuid).then(response => {
          this.$notify({
            title: "提示",
            message: "记录删除成功",
            type: "success",
            duration: 2000
          });
          const index = this.tableData.indexOf(row);
          this.tableData.splice(index, 1);
        });
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.pagination {
  padding: 20px 0;
}
</style>
