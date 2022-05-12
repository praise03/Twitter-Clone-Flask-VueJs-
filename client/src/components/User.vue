<template>
  <div class="flex container h-screen w-full p-2">

    <Sidebar></Sidebar>
    <main v-if="dataLoaded"  class="w-[77%] border-r-[1px] overflow-y-scroll">
    <div class="flex flex-center  ml-2 px-2">

            <i @click="s" class="fas fa-arrow-left cursor-pointer text-xl mr-10"></i>
            <div class="flex flex-col">
              <p class="font-semibold text-xl -mt-1">I have no idea what i'm doing</p>
              <p class="text-gray-600 -mt-1">964 Tweets</p>
            </div>
        </div>

        <div class="bg-twitterlightgray relative w-full h-52">
          <div class="absolute border-white mt-32 ml-6 rounded-full border-4">
            <img class="rounded-full h-32 w-32  " src="../assets/logo.png">
          </div>
        </div>

        <button v-if="userstore.userdata.username == route.params.username" class="px-3 py-1 mr-3 focus:outline-none hover:bg-slate-100 float-right ml-80 mt-3 border-1 border font-semibold  rounded-full">Edit Profile</button>
        <!-- <div  class="mt-12"> </div> -->
        <div class="flex flex-col mt-10 px-4 py-3">
          <p class="text-xl font-bold">{{ user.username }}</p>
          <p class="font-extralight -mt-1 text-twitterdarkgray">@{{user.email}}</p>
          <p class="text-md mt-2 font-light">about</p>
		    </div>
          <div class="py-2 px-3 flex justify-between mb-2 border-b">
            <span class="flex ml-1">
              <p class="mr-4 text-sm cursor-pointer font-extralight  hover:underline"><span class="font-bold text-md">{{user.following}}</span> Following</p>
              <p class="mr-4 text-sm cursor-pointer font-extralight hover:underline"><span class="font-bold text-md">{{user.followers}}</span> Followers</p>
            </span>
            <span v-if="userstore.userdata.username != route.params.username">
                 <button v-if="following" @click="unfollow()" class="border border-red-400 hover:bg-slate-100 focus:outline-none font-semibold px-4 py-1 -mt-2 rounded-2xl">Unfollow</button>  
			           <button v-else @click="follow()" class="border hover:bg-slate-100 focus:outline-none font-semibold px-4 py-1 -mt-2 rounded-2xl">Follow</button>
            </span>
          </div>
        

        <div v-for="post in posts" :key="post.id"  class="border-b cursor-pointer hover:bg-twitterxxlgray">
			<div @click="router.push({ path: '/tweet/' + post.id})"  class="flex p-4">
				<img src="../assets/android_0.jpg" class="w-12 h-12 rounded-full mr-4" alt="">
				
				<div class="w-full">
					<div class="flex">
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
      <div class="ml-16 mb-2 flex justify-between px-4 text-gray-400">
						<span class="cursor-pointer flex space-x-2 hover:text-blue-500"><i class="hover:bg-blue-300 p-1 rounded-full far fa-comment"></i><p class="mt-[0.2rem] text-sm font-extralight">{{post.no_of_comments}}</p></span>
						<span class="cursor-pointer flex space-x-2 hover:text-green-500"><i class="hover:bg-green-300 p-1 rounded-full fas fa-retweet"></i><p class="mt-[0.2rem] text-sm font-extralight">0</p></span>
						<span @click="like(post.id)" class="cursor-pointer flex space-x-2 hover:text-red-500"><i class="hover:bg-red-300 p-1 rounded-full far fa-heart"></i><p class="mt-[0.2rem] text-sm font-extralight">{{post.no_of_likes}}</p></span>
						<i class="fas fa-globe mt-1"></i>
			</div>
		</div>
    </main>

        <Trending />
  </div>
</template>


<script setup lang="ts">
import Sidebar from './Sidebar.vue';
import Trending from './Trending.vue'
import { userStore } from '../UserStore'
import { postStore } from '../PostStore'
import {ref, reactive} from 'vue'
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios'

  const userstore = userStore()
  const poststore = postStore()
  const route = useRoute()
  const router = useRouter() 

  const username = route.params.username
  const posts = ref([]);
  const user = ref({})
  const following = ref(false)
  const dataLoaded = ref(false)
	
	const fetchUser = async () => {
    const path = 'http://127.0.0.1:5000/api/user/profile'
		const res = await axios.post(path, {'username': username});
    if (res.data.error){
      router.replace('/404')
      return
    }
		posts.value = res.data.posts;
    user.value = res.data.user
		dataLoaded.value = true
		// console.log(post.value);
	}
  
	fetchUser()

  async function like(id:number){
    if (userstore.userdata.id != null) {
      userstore.validateToken().then( async() => {
        const token = userstore.userdata.token!
        const user = userstore.userdata.id!
        const tweet = id
        const response = await poststore.likeTweet(tweet, user, token) as unknown as string
        if (response == 'done') {
          fetchUser()	
        }
      } )
    }
	}

  const checkFollowing = async() => {
    if (userstore.userdata.id != null) {
      userstore.validateToken().then( async() => {
			const token = userstore.userdata.token!
			const currentUser = userstore.userdata.id!
      const user = route.params.username as string
			const response = await userstore.checkFollowing(currentUser, user, token) as unknown as string
			if (response == 'true') {
				following.value = true
			}
		} ) 
    }else{
      return
    }
  }
  if (route.params.username != userstore.userdata.username) {
    checkFollowing() 
  }

  const follow = async() => {
    if (userstore.userdata.id) {
      userstore.validateToken().then( async() => {
			const token = userstore.userdata.token!
			const currentUser = userstore.userdata.id!
      const user = route.params.username as string
			const response = await userstore.follow(currentUser, user, token) as unknown as string
			if (response == 'done') {
				following.value = true;
        fetchUser()
			}
		} ) 
    }
  }

  const unfollow = async() => {
    if (userstore.userdata.id) {
      userstore.validateToken().then( async() => {
			const token = userstore.userdata.token!
			const currentUser = userstore.userdata.id!
      const user = route.params.username as string
			const response = await userstore.unfollow(currentUser, user, token) as unknown as string
			if (response == 'done') {
				following.value = false;
        fetchUser()
			}
		} ) 
    }
  }


</script>
