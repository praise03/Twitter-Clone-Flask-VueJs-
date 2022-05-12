<template>
    <div class="absolute flex h-full w-screen inset-0 bg-gray-900 bg-opacity-50 z-50">
	<div class="m-auto flex-col bg-white p-20 text-center rounded-lg">
			<button @click="poststore.modal.hidden = false" class="ml-10 cursor-pointer absolute top-50 block -mt-12">X</button>
			<p class="p-2 text-xl font-bold mb-4">{{poststore.modal.body}}</p>
			<span v-if="poststore.modal.showSignIn">
				<button @click="router.push('/signin'); poststore.modal.hidden = false" class="text-white bg-twitterblue px-36 py-3 rounded-full">Login</button><br>
				<button @click="router.push('/signup'); poststore.modal.hidden = false" class="bg-white text-twitterblue px-[140px] py-3 mt-2 border rounded-full">Sign Up</button>
			</span>
		</div>
</div>
</template>

<script setup lang="ts">
    import {postStore} from '../PostStore'
	import {useRouter} from 'vue-router'
    const poststore = postStore()
	const router = useRouter()
</script>