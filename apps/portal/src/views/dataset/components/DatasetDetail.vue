<template>
  <div class="app-container">
    <el-form :model="ruleForm" :rules="rules" ref="ruleForm">
      <el-form-item label="名称" prop="title">
        <el-input v-model="ruleForm.title" placeholder="请输入内容"></el-input>
      </el-form-item>
      <el-form-item label="行业分类" prop="tag">
        <el-select v-model="ruleForm.tag" placeholder="请选择" style="width: 100%">
          <el-option v-for="item in tagOptions" :key="item" :label="item" :value="item"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="数据类型" prop="catalog">
        <el-select v-model="ruleForm.catalog" placeholder="请选择" style="width: 100%">
          <el-option
            v-for="item in catalogOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="板块运算" prop="mode">
        <el-select v-model="ruleForm.mode" placeholder="请选择" style="width: 100%">
          <el-option
            v-for="item in computeModeOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="面积运算" prop="inc_area">
        <el-switch v-model="ruleForm.inc_area"></el-switch>
      </el-form-item>
      <el-form-item label="选择文件" prop="data">
        <upload-excel-component :on-success="handleSuccess" :before-upload="beforeUpload" />
      </el-form-item>
      <el-form-item>
        <router-link :to="'/dataset/list'">
          <el-button>返 回</el-button>
        </router-link>
        <el-button
          type="primary"
          @click="isEdit?updateData():createData()"
        >保 存</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import UploadExcelComponent from "./UploadExcel/index.vue";
import { getList, getDetail, create, update, remove } from "@/api/dataset";

export default {
  name: "DatasetDetail",
  components: { UploadExcelComponent },
  props: {
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      tagOptions: [
        "交通设施",
        "政府机构",
        "教育培训",
        "旅游景点",
        "房地产",
        "购物",
        "美食",
        "医疗",
        "酒店"
      ],
      catalogOptions: [
        { value: "point", label: "集合数据" },
        { value: "block", label: "板块数据" }
      ],
      computeModeOptions: [
        { value: "$sum", label: "求和" },
        { value: "$avg", label: "平均" },
        { value: "$max", label: "最大" },
        { value: "$min", label: "最小" },
        { value: "$stdDevSamp", label: "标准偏差" }
      ],
      uuid: undefined,
      ruleForm: {
        title: "",
        catalog: "",
        mode: "",
        tag: "",
        inc_area: false,
        data: "",
        header: ""
      },
      rules: {
        title: [{ required: true, message: "请输入内容", trigger: "blur" }],
        catalog: [{ required: true, message: "请输入内容", trigger: "blur" }],
        mode: [{ required: true, message: "请输入内容", trigger: "blur" }],
        tag: [{ required: true, message: "请输入内容", trigger: "blur" }],
        inc_area: [{ required: true, message: "请输入内容", trigger: "blur" }],
        data: [{ required: true, message: "请输入内容", trigger: "blur" }]
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
    fetchDetail() {
      getDetail(this.uuid).then(response => {
        this.ruleForm = Object.assign({}, response);
      });
    },
    beforeUpload(file) {
      const isLt1M = file.size / 1024 / 1024 < 1;
      if (isLt1M) {
        return true;
      }
      this.$message({
        message: "Please do not upload files larger than 1m in size.",
        type: "warning"
      });
      return false;
    },
    handleSuccess({ results, header }) {
      this.ruleForm.data = results;
      this.ruleForm.header = header;
    },
    createData() {
      this.$refs["ruleForm"].validate(valid => {
        if (valid) {
          create(this.ruleForm).then(() => {
            this.$router.push({ path: "/dataset/list" });
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
            this.$router.push({ path: "/dataset/list" });
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
