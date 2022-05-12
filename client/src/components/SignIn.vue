<template>
    <div v-if="errorMessage.value" class="text-red-400 container text-center">
      <h1 class="p-4 text-lg  font-semibold">{{ errorMessage.message }}</h1>
    </div>
    <div v-if="accountCreated" class="text-green-400 container text-center">
      <h1 class="p-4 text-lg  font-semibold">Account created successfully. You can now Login</h1>
    </div>
    <form @submit.prevent="signIn"> 
    <div class="bg-gray-800 p-2 h-screen">
        <div class="bg-white flex flex-col lg:w-1/3 ml-auto mr-auto rounded-lg mt-32 justify-center items-center">
            <i class="fab fa-twitter text-blue-300 text-2xl p-4"></i>
            
            <h1 class="p-8 text-2xl font-bold">Sign in to Twitter</h1>

            <input type="text" v-model="userData.usernameOrEmail" placeholder="Email or Username" class="border py-2 px-16 text-grey-darkest mb-3 rounded-md" required>
            <div>
                <input :type="type" v-model="userData.password" placeholder="password" class="border py-2 px-16 mb-4 rounded-md" required>
                <button type="button" @click="toogle()"> <i class="fas fa-eye text-blue-800 -ml-8 cursor-pointer"></i> </button> 
            </div>
            <button class="bg-black px-36 rounded-2xl py-2 mb-4 text-white">Sign In</button>
            <router-link to="/signup" class="mb-16">Don't have an account? <a class="text-blue-400">Sign up</a></router-link>
        </div>
    </div>
    </form>
</template>


<script setup lang="ts">
	import { ref, reactive, onActivated } from 'vue'
	import { useRouter, useRoute } from 'vue-router'
	import axios from 'axios'
	import { userStore } from '../UserStore'

	interface Userdata {
		usernameOrEmail: string
		password: string;
	}

	
    const route = useRoute()
    const router = useRouter()
    const userstore = userStore()


    

	let type = ref('password')
	let accountCreated = ref(false)
	const userData: Userdata = reactive({
		usernameOrEmail: "",
		password: "",
	});
	const errorMessage= reactive({
		value: false,
		message: ''
	});

    if (route.query.account == 'created') {
        console.log(route.query)
		accountCreated.value = true
	}

	const toogle = () => {
        if (type.value == 'password') { type.value = 'text' } else { type.value = 'password' }
    }

	const signIn = async () => {
        const resp = await userstore.signin(userData.usernameOrEmail, userData.password)
        if (resp.error) {
            errorMessage.value = true,
            errorMessage.message = resp.error
        }else if(resp.success){
            router.push({path : '/'})
        }
	}

</script>

// import axios from "axios";
// import {ref} from 'vue'



// export default {
//   data() {
//     return {
//       type: "password",
//       userData: {
//         usernameOrEmail: "",
//         password: "",
//       },
//       errorMessage : {
//         value: false,
//         message: ''
//       },
//       accountCreated : false
//     };
//   },

//   methods: {
//     toogle(){
//         if (this.type == 'password') { this.type = 'text' } else { this.type = 'password' }
//     },

//     signIn() {
//         const path = "http://127.0.0.1:5000/api/signin/";
//         axios.post(path, this.userData).then((res) => {
//             if (res.data.error) {
//                 this.errorMessage.value = true
//                 this.errorMessage.message = res.data['error']
//             }else if(res.data.message){
//               const token = res.data.token
//               console.log(token)
//             }
            
//         }).catch((error) => {console.log(error)})
//     },
//   },

//   created(){
//     if (this.$route.query.account == 'created') {
//       this.accountCreated = true
//     }
//   }
// };