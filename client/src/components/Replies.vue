<template>
  <div class="flex container h-screen w-full p-2">

    <Sidebar />
    <main class="w-[77%] border-r-[1px] overflow-y-scroll" v-if="dataLoaded">
		<span class="flex flex-row py-1 px-4 mb-5 items-center">
		    <button @click="router.back()"><i class="fas fa-arrow-left cursor-pointer"></i></button>
			<p class="font-bold text-xl ml-12">Tweet</p>
		</span>

        <div class="cursor-pointer border-b hover:bg-twitterxxlgray">
			<div class="flex p-1">
				<img src="../assets/android_0.jpg" class="w-12 h-12 rounded-full mr-4" alt="">
				
				<div class="flex-col w-full">
					<div class="flex">
						<div class="flex-col">
							<h3 class="font-semibold text-md ">{{comment.author.username}}</h3>
							<p class="text-md font-light text-gray-400 -mt-1">{{comment.author.email}}</p>
						</div>
						<i class="fas fa-ellipsis text-gray-500 ml-auto mt-2"></i>
					</div>
				

				</div>
			</div>
			<span class="px-2 text-lg">
				{{comment.body}}
			</span>
			<div class="flex flex-row text-sm font-thin text-twitterdarkgray border-b px-2 mt-3 space-x-2">
				<p class="">7:18 AM</p>
				<i class="-mt-1">.</i>
				<p>Apr 25, 2022</p>
				<i class="-mt-1">.</i>
				<p class="mb-3">Twitter Web App</p>
			</div>
			<div class="flex flex-row text-twitterdarkgray text-md space-x-7 border-b py-3 mx-2">
				<p> <b class="text-black">39</b> Retweets</p>
				<p><b class="text-black">5</b> Likes</p>
			</div>
			<div class="flex justify-between mt-3 py-3 mx-8 text-xl text-twitterdarkgray">
				<span class="cursor-pointer flex space-x-2 hover:text-blue-500"><i class="hover:bg-green-300 p-1 rounded-full far fa-comment"></i></span>
				<span class="cursor-pointer flex space-x-2 hover:text-green-500"><i class="hover:bg-green-300 p-1 rounded-full fas fa-retweet"></i></span>
				<span class="cursor-pointer flex space-x-2 hover:text-red-500"><i class="hover:bg-red-300 p-1 rounded-full far fa-heart"></i></span>
				<i class="fas fa-globe mt-1"></i>
			</div>
		</div>
		<div>
			<div class="flex p-4">
				<img src="../assets/android_0.jpg" class="w-12 h-12 rounded-full mr-4" alt="">
			</div>
		</div>
		<div v-for="reply in replies" :key="reply.id" @click="router.push({ path: '/replies/' + reply.id})" class="hover:bg-gray-100 cursor-pointer border-t  border-b w-full px-4 py-2">
			<div class="flex">
				<h3 class="font-semibold text-md mr-2">{{ reply.author.username }}</h3>
				<p class="text-sm font-light text-gray-400 mt-[0.2rem] mr-3">@{{ reply.author.email }}</p>
				<p class="text-sm font-light text-gray-400 mt-[0.2rem] mr-2">18h</p>
				<i class="fas fa-ellipsis text-gray-500 ml-auto mt-2"></i>
				</div>

				<span class="text-sm py-2">
				{{ reply.body }}
				</span>
				<div class="flex justify-between mt-3 text-gray-400">
				<span class="cursor-pointer flex space-x-2 hover:text-blue-500"><i class="hover:bg-blue-300 p-1 rounded-full far fa-comment"></i><p class="mt-[0.2rem] text-sm font-extralight">{{ reply.replies }}</p></span>
				<span class="cursor-pointer flex space-x-2 hover:text-green-500"><i class="hover:bg-green-300 p-1 rounded-full fas fa-retweet"></i><p class="mt-[0.2rem] text-sm font-extralight">446</p></span>
				<span class="cursor-pointer flex space-x-2 hover:text-red-500"><i class="hover:bg-red-300 p-1 rounded-full far fa-heart"></i><p class="mt-[0.2rem] text-sm font-extralight">446</p></span>
				<i class="fas fa-globe mt-1"></i>
			</div>
        </div>

		
    </main>

        <Trending />
  </div>
</template>

<script setup lang="ts">
import { defineComponent, onMounted, reactive, ref , computed, watch } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from './Sidebar.vue'
import Trending from './Trending.vue' 

	interface Author{
		id: number,
        username: string,
        email: string
	}

	interface Post{
		id: number,
		body: string,
		timestamp: string,
		author: Author,
		no_of_likes: number,
		no_of_comments: number,
		comments: Array<Object>
	}

	// let post: Post
	const dataLoaded = ref(false)
	const  route = useRoute()
    const router = useRouter()
	const path = 'http://127.0.0.1:5000/api/fetch/replies'
	const comment = ref({});
    const replies = ref([])
	

	const c = async () => {
            const res = await axios.post(path, route.params.id)
            comment.value = res.data.comment;
            replies.value = res.data.replies
            dataLoaded.value = true
            console.log(replies.value);
	}

    const back = () => {
        route.params.c = comment.value.id
        console.log('r ' + route.params.c)
    }
   

    watch(
      () => route.params.id,
      async () => {
            const res = await axios.post(path, route.params.id);
            comment.value = res.data.comment;
            replies.value = res.data.replies
            dataLoaded.value = true
        }
    )
	c()




	

</script>
