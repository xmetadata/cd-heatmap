<template>
  <div class="app-container">
    <div class="filter-container" style="margin-bottom: 10px;">
      <el-select v-model="uuid" placeholder="请选择对象" style="width:200px;" @change="changeDataset()">
        <el-option
          v-for="item in datasetList.items"
          :key="item.uuid"
          :label="item.title"
          :value="item.uuid"
        ></el-option>
      </el-select>
      <span v-for="item in navigate" :key="item.label">
        <el-select
          v-model="match[item.label]"
          :placeholder="'请选择' + item.label"
          style="width:160px;"
          @change="changeDataset()"
        >
          <el-option v-for="item in item.options" :key="item" :label="item" :value="item"></el-option>
        </el-select>
      </span>
      <el-button
        class="filter-item"
        type="primary"
        icon="el-icon-search"
        @click="changeDataset()"
      >检索</el-button>
    </div>

    <baidu-map
      class="bm-view"
      :style="conheight"
      :center="center"
      :zoom="zoom"
      @ready="handler"
      :scroll-wheel-zoom="true"
      :mapStyle="mapStyle"
      ak="j1rB54xkUHAoEp41Z6FwXwyXVVgASoDE"
      v-loading="loading"
    >
      <!-- control BMAP_ANCHOR_TOP_LEFT -->
      <bm-control style="padding: 10px;">
        <button class="bm-button" @click="showPolygon()">
          <span v-if="polygonVision">集合模式</span>
          <span v-else>板块模式</span>
        </button>
        <button class="bm-button" @click="showMarker()">
          <span v-if="markerVision">隐藏标记</span>
          <span v-else>显示标记</span>
        </button>
      </bm-control>
      <!-- control BMAP_ANCHOR_BOTTOM_RIGHT -->
      <bm-control anchor="BMAP_ANCHOR_BOTTOM_RIGHT">
        <div style="background-color: #ffffff; padding:10px; margin:5px; border:1px solid #C0C0C0">
          <div v-if="polygonVision">
            <div v-for="(item, index) in blockColor" :key="item">
              <div v-if="index > 0">
                <div
                  :style="{width: '30px', height: '20px', display: 'inline-block', background: item}"
                ></div>
                <div
                  :style="{display: 'inline-block'}"
                >{{ Math.round(max * ( index-1 ) * 0.2) + ' - ' + Math.round(max * index * 0.2) }}</div>
              </div>
            </div>
          </div>
          <div v-else>
            <div v-for="(item, index) in heatmapColor" :key="item">
              <div
                :style="{width: '30px', height: '20px', display: 'inline-block', background: item}"
              ></div>
              <div
                :style="{display: 'inline-block'}"
              >{{ Math.round(max * index * 0.25) + '-' + Math.round(max * ( index + 1 ) * 0.25) }}</div>
            </div>
          </div>
        </div>
      </bm-control>
      <!-- polygon -->
      <bm-polygon
        v-for="polygon in polygonsData"
        :key="'polygon' + polygon.title + Math.random()"
        :path="polygon.coordinates"
        :massClear="false"
        :strokeWeight="1"
        stroke-color="red"
        fillColor
      />
      <!-- polygon -->
      <bm-polygon
        v-for="polygon in polygons"
        :key="'polygon' + polygon.title + Math.random()"
        :path="polygon.coordinates"
        :stroke-opacity="0.1"
        :strokeWeight="1"
        :fillColor="polygonVision?blockColor[Math.ceil(polygon.value / max * 10 / 2)]:''"
      />
      <span v-if="markerVision">
        <span v-for="polygon in polygons" :key="'label' + polygon.title">
          <bm-label
            v-if="polygon.value!==0"
            :content="polygonVision?polygon.title + '-' + Math.round(polygon.org_value):polygon.title"
            :position="polygon.centroid"
            :labelStyle="labelStyle"
            :offset="{width: -35, height: -15}"
          />
        </span>
      </span>
      <!-- heatmap -->
      <bml-heatmap :data="heatmap" :max="max" :radius="20"></bml-heatmap>
      <span v-if="markerVision">
        <bm-point-collection
          :points="heatmap"
          shape="BMAP_POINT_SHAPE_WATERDROP"
          @mouseover="mouseoverHandler"
          @mouseout="mouseoutHandler"
        />
      </span>
      <span v-if="labelVision">
        <bm-marker :position="marker" animation="BMAP_ANIMATION_BOUNCE">
          <bm-label
            :content="marker.title + ' ' + marker.value"
            :labelStyle="labelStyle"
            :offset="{width: 30, height: -10}"
          />
        </bm-marker>
      </span>
    </baidu-map>
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
} from "@/api/dataset";
import {
  BaiduMap,
  BmControl,
  BmLabel,
  BmMarker,
  BmlHeatmap,
  BmPolygon,
  BmPointCollection
} from "vue-baidu-map";

export default {
  components: {
    BaiduMap,
    BmControl,
    BmLabel,
    BmMarker,
    BmlHeatmap,
    BmPolygon,
    BmPointCollection
  },
  data() {
    return {
      loading: false,
      conheight: { height: "" },
      datasetList: [],
      uuid: null,
      navigate: null,
      match: {},
      center: { lng: 0, lat: 0 },
      zoom: 0,
      markerVision: false,
      marker: null,
      labelVision: false,
      polygonVision: true,
      max: 0,
      polygons: [],
      polygonsData: [],
      polygonsMax: 0,
      heatmap: [],
      heatmapData: [],
      heatmapMax: 0,
      labelStyle: {
        fontSize: "10px",
        background: "rgba(0,0,0,0.5)",
        color: "#fff",
        border: "none",
        padding: "2px",
        boxShadow: "0 0 2px #000"
      },
      blockColor: ["", "#F9EFA7", "#F2B78B", "#E97D6E", "#E95C59", "#D23943"],
      heatmapColor: ["#8484F2", "#66FF00", "#FFAA00", "#FF0000"],
      mapStyle: {
        featureType: "all",
        elementType: "all",
        stylers: {
          lightness: 10,
          saturation: -100
        }
      }
    };
  },
  mounted() {
    this.getHeight();
    this.fetchDataList();
  },
  methods: {
    getHeight() {
      this.conheight.height = window.innerHeight - 160 + "px";
    },
    handler({ BMap, map }) {
      this.map = map;
      this.center.lng = 108.953364;
      this.center.lat = 34.275946;
      this.zoom = 12;
    },
    fetchDataList() {
      getList().then(response => {
        this.datasetList = response;
      });
    },
    changeDataset() {
      for (let i = 0; i < this.datasetList.items.length; i++) {
        if (this.datasetList.items[i].uuid == this.uuid) {
          this.navigate = JSON.parse(this.datasetList.items[i].navigate);
        }
      }
      if (this.uuid === null || this.uuid === "") {
        this.$message({
          message: "未选择数据对象",
          type: "warning",
          duration: 2 * 1000
        });
        return;
      }
      // reset configuration
      this.polygonVision = true;
      this.markerVision = false;
      this.match = {};
      // loading block
      this.loading = true;
      getData(this.uuid, { catalog: "block", match: this.match }).then(
        response => {
          this.polygonsData = response.items;
          this.polygonsMax = response.max;
          this.loading = false;
          this.showOverlay();
        }
      );
      // loading point
      this.loading = true;
      getData(this.uuid, { catalog: "point", match: this.match }).then(
        response => {
          this.heatmapData = response.items;
          this.heatmapMax = response.max;
          this.loading = false;
        }
      );
    },
    mouseoverHandler(e) {
      this.marker = e.point;
      this.marker.title = "";
      for (let i = 0; i < this.heatmap.length; i++) {
        if (
          this.marker.lng === this.heatmap[i].lng &&
          this.marker.lat === this.heatmap[i].lat
        ) {
          this.marker.title = this.heatmap[i].title;
          this.marker.value = this.heatmap[i].value;
          break;
        }
      }
      this.labelVision = true;
    },
    mouseoutHandler(e) {
      this.marker = null;
      this.labelVision = false;
    },
    showPolygon() {
      this.markerVision = false;
      if (this.polygonVision) {
        this.polygonVision = false;
      } else {
        this.polygonVision = true;
      }
      this.showOverlay();
    },
    showMarker() {
      if (this.markerVision) {
        this.markerVision = false;
      } else {
        this.markerVision = true;
      }
    },
    showOverlay() {
      // clearOverlays
      this.map.clearOverlays();
      this.markerVision = false;

      if (this.polygonVision) {
        this.heatmap = [];
        this.polygons = this.polygonsData;
        this.max = this.polygonsMax;
      } else {
        this.polygons = [];
        this.heatmap = this.heatmapData;
        this.max = this.heatmapMax;
      }
    }
  }
};
</script>

<style>
.bm-view {
  width: 100%;
  height: 500px;
}
.bm-button {
  background-color: #3f51b5;
  color: rgba(255, 255, 255, 0.87);
  outline: none;
  min-width: 88px;
  min-height: 36px;
  margin: 6px 8px;
  padding: 0 16px;
  display: inline-block;
  position: relative;
  overflow: hidden;
  user-select: none;
  cursor: pointer;
  border: 0;
  border-radius: 2px;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  font-family: inherit;
  font-size: 14px;
  font-style: inherit;
  font-variant: inherit;
  font-weight: 500;
  letter-spacing: inherit;
  line-height: 36px;
  text-align: center;
  text-transform: uppercase;
  text-decoration: none;
  vertical-align: top;
  white-space: nowrap;
}
</style>
