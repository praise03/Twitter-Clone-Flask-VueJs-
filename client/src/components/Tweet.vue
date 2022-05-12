<template>
  <div class="flex container h-screen w-full p-2">

    <Sidebar />
    <main class="w-[77%] border-r-[1px] overflow-y-scroll" v-if="dataLoaded">
		<span class="flex flex-row py-1 px-4 mb-5 items-center">
			<button @click="router.back()"><i class="fas fa-arrow-left"></i></button>
			<p class="font-bold text-xl ml-12">Tweet</p>
		</span>

        <div class="cursor-pointer border-b hover:bg-twitterxxlgray">
			<div class="flex p-1">
				<img src="../assets/android_0.jpg" class="w-12 h-12 rounded-full mr-4" alt="">
				
				<div class="flex-col w-full">
					<div class="flex">
						<div class="flex-col">
							<h3 class="font-semibold text-md ">{{post.author.username}}</h3>
							<p class="text-md font-light text-gray-400 -mt-1">{{post.author.email}}</p>
						</div>
						<i class="fas fa-ellipsis text-gray-500 ml-auto mt-2"></i>
					</div>
				

				</div>
			</div>
			<span class="px-2 text-lg">
				{{post.body}}
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
				<p><b class="text-black">{{post.no_of_likes}}</b> Likes</p>
			</div>
			<div class="flex justify-between mt-3 py-3 mx-8 text-xl text-twitterdarkgray">
				<span class="cursor-pointer flex space-x-2 hover:text-blue-500"><i class="hover:bg-green-300 p-1 rounded-full far fa-comment"></i></span>
				<span class="cursor-pointer flex space-x-2 hover:text-green-500"><i class="hover:bg-green-300 p-1 rounded-full fas fa-retweet"></i></span>
				<span class="cursor-pointer flex space-x-2 hover:text-red-500"><i class="hover:bg-red-300 p-1 rounded-full far fa-heart"></i></span>
				<i class="fas fa-globe mt-1"></i>
			</div>
		</div>
		<div>
			<div v-if="userstore.userdata.id != null" class="flex p-4 border-b">
				<img src="../assets/android_0.jpg" class="w-12 h-12 rounded-full mr-4" alt="">
				<input v-model="body" type="textarea" placeholder="Type Something" class="focus:outline-none w-full" cols="128" rows="2" >
				<input type="submit" value="Tweet" @click="comment(post.id)" class="px-6 py-1 bg-twitterblue text-white rounded-full cursor-pointer">
			</div>
		</div>
		<!-- <div v-for="comment in post.comments" :key="comment.id" @click="router.push({ name: 'replies', params: { c: comment.id }})" class="hover:bg-gray-100 cursor-pointer border-t  border-b w-full px-4 py-2"> -->
		<div v-for="comment in post.comments" :key="comment.id"  class="border-b cursor-pointer hover:bg-twitterxxlgray">
			<div @click="router.push({ path: '/replies/' + comment.id})"  class="flex p-4">
				<img src="../assets/android_0.jpg" class="w-12 h-12 rounded-full mr-4" alt="">
				
				<div class="w-full">
					<div class="flex mb-2">
						<h3 class="font-semibold text-md mr-2">{{ comment.author.username }}</h3>
						<p class="text-sm font-light text-gray-400 mt-[0.2rem] mr-3">@{{ comment.author.email }}</p>
						<p class="text-sm font-light text-gray-400 mt-[0.2rem] mr-2">18h</p>
						<i class="fas fa-ellipsis text-gray-500 ml-auto mt-2"></i>
					</div>

					<span class="text-sm">
						{{comment.body}}
					</span>
					
				</div>
			</div>
      		<div class="ml-16 mb-1 flex justify-between px-4 text-gray-400">
				<span class="cursor-pointer flex space-x-2 hover:text-blue-500"><i class="hover:bg-blue-300 p-1 rounded-full far fa-comment"></i><p class="mt-[0.2rem] text-sm font-extralight">{{ comment.replies }}</p></span>
				<span class="cursor-pointer flex space-x-2 hover:text-green-500"><i class="hover:bg-green-300 p-1 rounded-full fas fa-retweet"></i><p class="mt-[0.2rem] text-sm font-extralight">446</p></span>
				<span v-if="comment.liked"  @click="likeComment(comment.id)" class="mt-1 cursor-pointer flex space-x-2 text-red-500"><i class=" rounded-full fas fa-heart"></i><p class=" text-sm font-extralight">{{comment.no_of_likes}}</p></span>
				<span v-else @click="likeComment(comment.id)" class="cursor-pointer flex space-x-2 hover:text-red-500"><i class="hover:bg-red-300 p-1 rounded-full far fa-heart"></i><p class="mt-[0.2rem] text-sm font-extralight">{{comment.no_of_likes}}</p></span>
				<i class="fas fa-share-square mt-1"></i>
			</div>
		</div>

		
    </main>

        <Trending />
  </div>
</template>

<script setup lang="ts">
import { defineComponent, onMounted, reactive, ref , computed } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { userStore } from '../UserStore'
import { postStore } from '../PostStore'
import Sidebar from './Sidebar.vue'
import Trending from './Trending.vue' 

	// interface Author{
	// 	id: number,
    //     username: string,
    //     email: string
	// }

	// interface Post{
	// 	id: number,
	// 	body: string,
	// 	timestamp: string,
	// 	author: Author,
	// 	no_of_likes: number,
	// 	no_of_comments: number,
	// 	comments: Array<Object>
	// }

	// let post: Post
	const dataLoaded = ref(false)
	const  route = useRoute()
	const router = useRouter()
	const path = 'http://127.0.0.1:5000/api/fetch/post'
	const post = ref({});
	const body = ref('')
	const userstore = userStore()
	const poststore = postStore()
	
	const fetchTweet = async () => {
		if(userstore.userdata.id){
			const res = await axios.post(path, {'post_id': route.params.id, 'user': userstore.userdata.id});
			post.value = res.data;
			dataLoaded.value = true
		}else{
			const res = await axios.post(path, {'post_id': route.params.id});
			post.value = res.data;
			dataLoaded.value = true
		}
	}
	fetchTweet()
	
	async function comment(id:number){
		userstore.validateToken().then( async() => {
			const token = userstore.userdata.token!
			const user = userstore.userdata.id!
      		const tweet = id
			const response = await poststore.comment(body.value, user, tweet, token) as unknown as string
			if (response == 'success') {
				body.value = ''
				fetchTweet()	
			}
		} )
	}

	async function likeComment(id:number){
		if (userstore.userdata.id == null) {
			poststore.modal.showSignIn = true;
			poststore.modal.body = 'Join Twitter To Like This Tweet'
			poststore.modal.hidden = true
			return
		}
		userstore.validateToken().then( async() => {
			const token = userstore.userdata.token!
			const user = userstore.userdata.id!
      		const comment = id
			const response = await poststore.likeComment(user, comment , token) as unknown as string
			if (response == 'done') {
				fetchTweet()	
			}
		} )
	}






	

</script>
