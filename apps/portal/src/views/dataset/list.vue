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
      <router-link :to="'/dataset/create'">
        <el-button
          class="filter-item"
          style="margin-left: 10px;"
          type="primary"
          icon="el-icon-plus"
        >添加</el-button>
      </router-link>
      <el-button type="text" @click="templateBlock()" style="margin-left:10px">下载板块模板</el-button>
      <el-button type="text" @click="templatePoint()">下载集合模板</el-button>
    </div>

    <el-table v-loading="listLoading" :data="tableData" style="width: 100%">
      <el-table-column fixed prop="title" label="名称"></el-table-column>
      <el-table-column fixed prop="tag" label="归属行业"></el-table-column>
      <el-table-column fixed prop="catalog" label="数据类型">
        <template slot-scope="scope">{{ scope.row.catalog=="point"?"集合":"板块" }}</template>
      </el-table-column>
      <el-table-column fixed="right" label="操作">
        <template slot-scope="scope">
          <span v-if="scope.row.complete">
            <el-button type="primary" size="small" icon="el-icon-download" title="数据导出" circle @click="handleDownload(scope.row)"></el-button>
            <el-button
              type="danger"
              size="small"
              icon="el-icon-delete"
              title="删除数据"
              circle
              @click="handleDelete(scope.row)"
            ></el-button>
          </span>
          <span v-else>
            <el-button size="small" icon="el-icon-loading" title="加载中..." circle></el-button>
          </span>
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
import { getList, getDetail, getData, create, update, remove } from "@/api/dataset";

export default {
  name: "DatasetList",
  data() {
    return {
      listLoading: true,
      total: 0,
      listQuery: {
        page: 1,
        pre_page: 10,
        title: undefined
      },
      tableData: [],
      downloadData: undefined
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
    },
    templateBlock() {
      import('./components/Export2Excel').then(excel => {
          const tHeader = ["板块", "数值"]
          const data = []
          excel.export_json_to_excel({
            header: tHeader,
            data,
            filename: '板块数据模板'
          })
          this.listLoading = false
        })
    },
    templatePoint() {
      import('./components/Export2Excel').then(excel => {
          const tHeader = ["标题", "地址", "经度", "纬度", "板块", "数值"]
          const data = []
          excel.export_json_to_excel({
            header: tHeader,
            data,
            filename: '集合数据模板'
          })
          this.listLoading = false
        })
    },
    handleDownload(row) {
      this.listLoading = true
      getDetail(row.uuid).then(response => {
        this.downloadData = response;
        import('./components/Export2Excel').then(excel => {
          const tHeader = JSON.parse(this.downloadData.headers)
          const data = this.formatJson(tHeader, this.downloadData.data)
          excel.export_json_to_excel({
            header: tHeader,
            data,
            filename: this.downloadData.title
          })
          this.listLoading = false
        })
      })
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => v[j]))
    }
  }
};
</script>

<style lang="scss" scoped>
.pagination {
  padding: 20px 0;
}
</style>
