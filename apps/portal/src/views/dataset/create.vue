<template>
  <dataset-detail :is-edit="false" />
</template>

<script>
import DatasetDetail from "./components/DatasetDetail";

export default {
  name: "DatasetCreate",
  components: { DatasetDetail }
};
</script>

