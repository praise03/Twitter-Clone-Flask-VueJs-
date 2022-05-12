<script setup lang="ts">
import Modal from './components/Modal.vue'
import { postStore } from './PostStore'
import {ref, watch} from 'vue'
const poststore = postStore()

const modal = ref(poststore.modal.hidden)

watch(
  () => poststore.modal.hidden, () => {
    modal.value = poststore.modal.hidden
  }
)


</script>


<template>
  <Modal v-if="modal" />
  <router-view />
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
