<template>
<div class="flex  h-screen w-full p-2">
	
    <Sidebar/>

	<main class="xl:w-[77%] sm:w-[670px] border-r-[1px] overflow-y-scroll z-50">
		
            <div class="absolute flex h-full w-screen inset-0 bg-gray-900 bg-opacity-50 ">
            <div class="m-auto flex-col bg-white p-20 text-center rounded-lg">
                    <p class="p-2 text-2xl font-bold mb-4">404</p>
                    <p class="p-2 text-xl font-bold mb-4">This Page Does Not Exist!</p>

                    <button @click="router.back()" class="bg-white text-twitterblue px-[140px] py-3 mt-5 border rounded-full"><i class="fas fa-left"></i> Go Back</button>
                </div>
        </div>
        
		
	</main>

	<Trending />
</div>
</template>

<script setup lang="ts">
import Sidebar from './Sidebar.vue';
import Trending from './Trending.vue'
import {useRouter} from 'vue-router'
const router = useRouter()
</script>
