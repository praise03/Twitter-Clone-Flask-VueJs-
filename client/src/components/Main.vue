<template>
<div class="flex  h-screen w-full p-2">
	
    <Sidebar/>

	<main class="xl:w-[77%] sm:w-[670px] border-r-[1px] overflow-y-scroll">
		
		<!-- <Feed /> -->
		<Feed/>
		
		
	</main>

	<Trending />
</div>
</template>

<script setup lang="ts">
import Sidebar from './Sidebar.vue';
import Trending from './Trending.vue'
import Feed from './Feed.vue'
import Modal from './Modal.vue'
</script>

<style scoped>

</style>
