<template>
    <div class="hidden sm:block xl:hidden sm:pl-2 w-[10%] pl-[9rem] border-r-[1px]">          
        <i @click="showModal()" class="fab fa-twitter text-3xl font-bold text-twitterblue mb-4 hover:bg-blue-200 rounded-full p-2 cursor-pointer"></i>

        <ul class="space-y-4 font-thin fa-thin text-xl">
            <router-link to="/" class="hover:bg-gray-300 cursor-pointer py-2 px-3 w-2/3 rounded-full"><i class="fas fa-home "></i></router-link>
            <li class="hover:bg-gray-300 cursor-pointer py-2 px-3 w-2/3 rounded-full"><i class="fas fa-hashtag mr-4 "></i></li>
            <li class="hover:bg-gray-300 cursor-pointer py-2 px-3 w-2/3 rounded-full"><i class="far fa-bell mr-4 "></i></li>
            <li class="hover:bg-gray-300 cursor-pointer py-2 px-3 w-2/3 rounded-full"><i class="far fa-envelope mr-4 "></i></li>
            <li class="hover:bg-gray-300 cursor-pointer py-2 px-3 w-2/3 rounded-full"><i class="far fa-bookmark mr-4 "></i></li>
            <li class="hover:bg-gray-300 cursor-pointer py-2 px-3 w-2/3 rounded-full"><i class="fas fa-list mr-4 "></i></li>
            <li @click="toProfile()" class="hover:bg-gray-300 cursor-pointer py-2 px-3 w-2/3 rounded-full"><i class="far fa-user mr-4 "></i></li>
            <span v-if="show">
                <li @click="router.push('/signin')" v-if="userstore.userdata.id == null" class="hover:bg-gray-300 cursor-pointer py-2 px-3 w-2/3 rounded-full"><i class="fas fa-arrow-right-to-bracket"></i></li>
                <li @click="signOut" v-else class="hover:bg-gray-300 cursor-pointer py-2 px-3 w-2/3 rounded-full"><i class="fas fa-arrow-right-from-bracket"></i></li>
            </span>
            <li @click="show = !show" class="hover:bg-gray-300 cursor-pointer py-2 px-3 w-2/3 rounded-full"><i class="fas fa-ellipsis mr-4 "></i></li>
            <button class="text-white px-4 py-3 bg-twitterblue rounded-3xl"><i class="fab fa-twitter"></i></button>
        </ul>

        <div class="flex mt-20">
            <img src="../assets/logo.png" class="rounded-full h-10 w-12 mr-2" alt="">
        </div>
    </div>
    
    <div class="hidden xl:block w-[43%] pl-[9rem] border-r-[1px]">          
        <i @click="showModal" class="fab fa-twitter text-3xl font-bold text-twitterblue mb-4 hover:bg-blue-200 rounded-full p-2 cursor-pointer"></i>

        <ul class="space-y-4 font-thin fa-thin text-xl">
            <router-link to="/" class="hover:bg-gray-300 cursor-pointer py-2 px-3 w-2/3 rounded-full"><i class="fas fa-home mr-4 "></i>Home</router-link>
            <li class="hover:bg-gray-300 cursor-pointer py-2 px-3 w-2/3 rounded-full"><i class="fas fa-hashtag mr-4 "></i>Explore</li>
            <li class="hover:bg-gray-300 cursor-pointer py-2 px-3 w-2/3 rounded-full"><i class="far fa-bell mr-4 "></i>Notifications</li>
            <li class="hover:bg-gray-300 cursor-pointer py-2 px-3 w-2/3 rounded-full"><i class="far fa-envelope mr-4 "></i>Messages</li>
            <li class="hover:bg-gray-300 cursor-pointer py-2 px-3 w-2/3 rounded-full"><i class="far fa-bookmark mr-4 "></i>Bookmarks</li>
            <li class="hover:bg-gray-300 cursor-pointer py-2 px-3 w-2/3 rounded-full"><i class="fas fa-list mr-4 "></i>Lists</li>
            <li @click="toProfile()" class="hover:bg-gray-300 cursor-pointer py-2 px-3 w-2/3 rounded-full"><i class="far fa-user mr-4 "></i>Profile</li>
            <span class="py-[2px]" v-if="show">
                <li @click="router.push('/signin')" v-if="userstore.userdata.id == null" class="hover:bg-gray-300 cursor-pointer py-2 px-3 w-2/3 rounded-full"> <i class="fas fa-arrow-right-to-bracket"></i> Sign In</li>
                <li @click="signOut" v-else class="hover:bg-gray-300 cursor-pointer py-2 px-3 w-2/3 rounded-full"> <i class="fas fa-right-from-bracket"></i> Sign Out</li>
            </span>
            <li @click="show = !show" class="hover:bg-gray-300 cursor-pointer py-2 px-3 w-2/3 rounded-full"><i class="fas fa-ellipsis mr-4 "></i>More</li>
            <button class="text-white px-20 py-3 bg-twitterblue rounded-3xl">Tweet</button>
        </ul>

        <div class="flex mt-20">
            <img src="../assets/logo.png" class="rounded-full h-10 w-12 mr-2" alt="">
            <div class="flex-col text-sm">
                <p class="font-bold ">User 001</p>
                <p>@user_01</p>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { userStore } from '../UserStore'
import { useRouter, useRoute } from 'vue-router'
import {ref} from 'vue'
import { postStore } from '../PostStore'
const userstore = userStore()
const router = useRouter()
const show = ref(false)
const poststore = postStore()

const toProfile = () => {
    router.push('/user/' + userstore.userdata.username)
}

const signOut = () => { userstore.signOut(); router.push('/signin') }

const showModal = () => {poststore.modal = true; console.log(poststore.modal)}
</script>
