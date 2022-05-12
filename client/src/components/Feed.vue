<template>
	<div>
   	 	<div class="container p-2" >
			<div class="flex items-baseline justify-between">
				<h1 class="font-bold text-xl ml-2">Home</h1>
				<i class="fas fa-star"></i>
			</div>
		</div>
		<div class="flex p-4  border-b">
			<img src="../assets/android_0.jpg" class="w-12 h-12 rounded-full mr-4" alt="">
			
			<form @submit.prevent="createTweet()" class="w-full mt-4 space-y-4">
				<input v-model="body" type="textarea" maxlength="250" cols="128" rows="2" placeholder="What's Happening?" class="-mt-2 w-full focus:outline-none text-bold">
				<p class="border-b pb-2 text-twitterblue text-sm font-bold">	<i class="fas fa-globe mr-2"></i>Everyone can reply </p>
				<div class="flex flex-row text-twitterblue justify-between p-1">
					<div class="-mt-2">
						<i class="far fa-image hover:bg-blue-200 p-2 cursor-pointer rounded-full"></i>
						<i class="fas fa-film hover:bg-blue-200 p-2 cursor-pointer rounded-full"></i>
						<i class="far fa-chart-bar hover:bg-blue-200 p-2 cursor-pointer rounded-full"></i>
						<i class="far fa-smile hover:bg-blue-200 p-2 cursor-pointer rounded-full"></i>
						<i class="fas fa-calendar-clock hover:bg-blue-200 p-2 cursor-pointer rounded-full"></i>
						<i class="fas fa-location-dot hover:bg-blue-200 p-2 cursor-pointer rounded-full"></i>
					</div>
					
					<input type="submit" class="text-white px-4 py-1 bg-twitterblue hover:bg-blue-500 rounded-3xl -mt-2" value="Tweet">
				</div>
			</form>
		</div>
		
		<div v-if="dataLoaded">
		<div v-for="post in posts" :key="post.id"  class="border-b cursor-pointer hover:bg-twitterxxlgray">
			<div @click="router.push({ path: '/tweet/' + post.id})"  class="flex p-4">
				<img src="../assets/android_0.jpg" class="w-12 h-12 rounded-full mr-4" alt="">
				
				<div class="w-full">
					<div class="flex mb-2">
						<h3 class="font-semibold text-md mr-2">{{post.author.username}}</h3>
						<p class="text-sm font-light text-gray-400 mt-[0.2rem] mr-3">{{post.author.email}}</p>
						<p class="text-sm font-light text-gray-400 mt-[0.2rem] mr-2">18h</p>
						<i class="fas fa-ellipsis text-gray-500 ml-auto mt-2"></i>
					</div>

					<span class="text-sm">
						{{post.body}}
					</span>
					
				</div>
			</div>
      		<div class="ml-16 mb-1 flex justify-between px-4 text-gray-400">
				<span @click="router.push({ path: '/tweet/' + post.id})" class="cursor-pointer flex space-x-2 hover:text-blue-500"><i class="hover:bg-blue-300 p-1 rounded-full far fa-comment"></i><p class="mt-[0.2rem] text-sm font-extralight">{{post.no_of_comments}}</p></span>
				<span class="cursor-pointer flex space-x-2 hover:text-green-500"><i class="hover:bg-green-300 p-1 rounded-full fas fa-retweet"></i><p class="mt-[0.2rem] text-sm font-extralight">0</p></span>
				<span v-if="post.liked"  @click="like(post.id)" class="mt-[5px] cursor-pointer flex space-x-2 text-red-500"><i class=" rounded-full fas fa-heart"></i><p class="mt-[-0.06rem] text-sm font-extralight">{{post.no_of_likes}}</p></span>
				<span v-else @click="like(post.id)" class="cursor-pointer flex space-x-2 hover:text-red-500"><i class="hover:bg-red-300 p-1 rounded-full far fa-heart"></i><p class="mt-[0.2rem] text-sm font-extralight">{{post.no_of_likes}}</p></span>
				<i class="fas fa-globe mt-1"></i>
			</div>
		</div>
		</div>
	</div>
</template>

<script setup lang="ts">
	import { ref } from 'vue'
	import { useRouter, useRoute } from 'vue-router'
	import { userStore } from '../UserStore'
	import { postStore } from '../PostStore'
	import axios from 'axios'


	interface Post {
		id: number,
		body: string,
		timestamp: string,
		author: any,
		no_of_likes: number,
		no_of_comments: number
	}



	const dataLoaded = ref(false)

	const  route = useRoute()
	const router = useRouter()
	const userstore = userStore()
	const poststore = postStore()
	
	const path = 'http://127.0.0.1:5000/api/fetch/feed';
	const posts = ref([]);
	const body = ref('')
	

	const log = () => {poststore.modal.hidden = true ;console.log(poststore.modal)}
	
	const fetchFeed = async () => {
		if (userstore.userdata.id != null) {
			const res = await axios.post(path, {'user': userstore.userdata.id});
			posts.value = res.data;
			dataLoaded.value = true
		}else{
			const res = await axios.get(path);
			posts.value = res.data;
			dataLoaded.value = true
		}
	}

	fetchFeed()

	async function createTweet(){
		if (userstore.userdata.id == null) {
			poststore.modal.showSignIn = true;
			poststore.modal.body = 'Join Twitter To Share Your Thoughts'
			poststore.modal.hidden = true
			return
		}
		userstore.validateToken().then( async() => {
			const token = userstore.userdata.token!
			const author = userstore.userdata.id!
			console.log(token)
			const response = await poststore.createTweet(body.value, author, token) as unknown as string
			console.log(response)
			if (response == 'success') {
				body.value = ''
				fetchFeed()	
			}

		} )
	}

	async function like(id:number){
		if (userstore.userdata.id == null) {
			poststore.modal.showSignIn = true;
			poststore.modal.body = 'Join Twitter To Like This Tweet'
			poststore.modal.hidden = true
			return
		}
		userstore.validateToken().then( async() => {
			const token = userstore.userdata.token!
			const user = userstore.userdata.id!
      		const tweet = id
			const response = await poststore.likeTweet(tweet, user, token) as unknown as string
			if (response == 'done') {
				fetchFeed()	
			}
		} )
	}
	
    

</script>