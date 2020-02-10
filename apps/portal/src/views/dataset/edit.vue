<template>
  <dataset-detail :is-edit="true" />
</template>

<script>
import DatasetDetail from "./components/DatasetDetail";

export default {
  name: "DatasetEdit",
  components: { DatasetDetail }
};
</script>

