<template>
  <div class="app-container">
    <el-form :model="ruleForm" :rules="rules" ref="ruleForm">
      <el-form-item label="板块名称" prop="title">
        <el-input v-model="ruleForm.title" placeholder="请输入内容"></el-input>
      </el-form-item>
      <el-form-item label="板块名称" prop="title">
        <baidu-map
          class="bm-view"
          :style="conheight"
          :center="ruleForm.centroid"
          :zoom="zoom"
          :scroll-wheel-zoom="true"
          @ready="handler"
          ak="j1rB54xkUHAoEp41Z6FwXwyXVVgASoDE"
          v-loading="loading"
        >
          <bm-polygon :path="ruleForm.coordinates" :editing="true" @lineupdate="updatePolygonPath"></bm-polygon>
        </baidu-map>
      </el-form-item>
      <el-form-item>
        <router-link :to="'/blockset/list'">
          <el-button>返 回</el-button>
        </router-link>
        <el-button type="primary" @click="isEdit?updateData():createData()">保 存</el-button>
      </el-form-item>
    </el-form>
    {{ ruleForm }}
  </div>
</template>

<script>
import { BaiduMap, BmPolygon } from "vue-baidu-map";
import { getList, getDetail, create, update, remove } from "@/api/blockset";

export default {
  components: {
    BaiduMap,
    BmPolygon
  },
  name: "BlocksetDetail",
  props: {
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      loading: false,
      uuid: undefined,
      map: undefined,
      conheight: { height: "500px" },
      zoom: 14,
      ruleForm: {
        centroid: {lng: 108.953364, lat: 34.275946},
        coordinates: [{lng: 108.978157, lat: 34.257688}, {lng: 108.930152, lat: 34.256972}, {lng: 108.954011, lat: 34.282986}]
      },
      rules: {
        title: [{ required: true, message: "请输入内容", trigger: "blur" }]
      }
    };
  },
  created() {
    if (this.isEdit) {
      this.uuid = this.$route.params && this.$route.params.uuid;
      this.fetchDetail();
    }
  },
  methods: {
    handler({ BMap, map }) {
      this.map = map;
    },
    updatePolygonPath(e) {
      this.ruleForm.coordinates = e.target.getPath();
    },
    getHeight() {
      this.conheight.height = window.innerHeight - 100 + "px";
    },
    fetchDetail() {
      getDetail(this.uuid).then(response => {
        this.ruleForm = Object.assign({}, response);
      });
    },
    createData() {
      this.$refs["ruleForm"].validate(valid => {
        if (valid) {
          create(this.ruleForm).then(() => {
            this.$router.push({ path: "/blockset/list" });
            this.$notify({
              title: "提示",
              message: "这条记录创建成功",
              type: "success",
              duration: 2000
            });
          });
        }
      });
    },
    updateData() {
      this.$refs["ruleForm"].validate(valid => {
        if (valid) {
          update(this.uuid, this.ruleForm).then(() => {
            this.$router.push({ path: "/blockset/list" });
            this.$notify({
              title: "提示",
              message: "这条记录修改成功",
              type: "success",
              duration: 2000
            });
          });
        }
      });
    }
  }
};
</script>
