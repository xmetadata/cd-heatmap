<template>
  <div class="app-container">
    <baidu-map
      class="bm-view"
      :style="conheight"
      :center="polygonCenter"
      :zoom="zoom"
      :scroll-wheel-zoom="true"
      @ready="handler"
      ak="j1rB54xkUHAoEp41Z6FwXwyXVVgASoDE"
      v-loading="loading"
    >
      <bm-polygon :path="polygonPath"></bm-polygon>
      <bm-label
        v-if="polygonCenter!=='' && polygonCenter!== null"
        :content="content"
        :position="polygonCenter"
        :labelStyle="labelStyle"
        :offset="{width: -30, height: -10}"
      />
    </baidu-map>
  </div>
</template>

<script>
import { getList, getDetail, create, update, remove } from "@/api/blockset";
import { BaiduMap, BmPolygon, BmLabel } from "vue-baidu-map";

export default {
  components: {
    BaiduMap,
    BmPolygon,
    BmLabel
  },
  data() {
    return {
      loading: false,
      uuid: null,
      polygonPath: [],
      polygonCenter: null,
      content: null,
      conheight: { height: "" },
      zoom: 0,
      labelStyle: {
        background: "rgba(0,0,0,0.5)",
        color: "#fff",
        border: "none",
        padding: "5px",
        boxShadow: "0 0 2px #000"
      }
    };
  },
  created() {
    this.uuid = this.$route.params && this.$route.params.uuid;
    this.fetchDetail(this.uuid);
    this.getHeight();
  },
  methods: {
    getHeight() {
      this.conheight.height = window.innerHeight - 100 + "px";
    },
    fetchDetail(uuid) {
      getDetail(uuid).then(response => {
        this.polygonCenter = JSON.parse(response.centroid);
        this.polygonPath = JSON.parse(response.coordinates);
        this.content = response.title;
      });
    },
    handler({ BMap, map }) {
      this.map = map;
      this.zoom = 14;
    }
  }
};
</script>
