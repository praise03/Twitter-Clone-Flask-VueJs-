<template>
  <div>
  <div v-if="errorMessage.value" class="text-red-400 container text-center">
    <h1 class="p-4 text-lg  font-semibold">{{ errorMessage.message }}</h1>
  </div>

  <form @submit.prevent="signUp()">
  <div class="bg-gray-800 p-2 h-screen ">
    <div
      class="
        bg-white
        flex flex-col
        lg:w-1/3
        ml-auto
        mr-auto
        rounded-lg
        justify-center
        items-center
        mt-32  z-50 backdrop-blur-3xl bg-white/90"
    >
      <i class="fab fa-twitter text-blue-300 text-2xl p-4"></i>

      <h1 class="p-8 text-2xl font-bold">Sign up for Twitter</h1>

      <input
        type="text"
        v-model="userData.username"
        placeholder="Username..."
        class="border py-2 px-16 text-grey-darkest mb-3 rounded-md"
        required
      />
      <input
        type="text"
        v-model="userData.email"
        placeholder="Email..."
        class="border py-2 px-16 text-grey-darkest mb-3 rounded-md"
        required
      />
	  <div>
      <input
        :type="type"
        v-model="userData.password"
        placeholder="Password"
        class="border py-2 px-16 mb-4 rounded-md"
        required
      />
	  <button type="button" @click.prevent="toogle"> <i class="fas fa-eye text-blue-800 -ml-8 cursor-pointer"></i> </button> 
	  </div>
      <input type="submit" value="Sign Up"
        class="bg-black px-36 rounded-2xl py-2 mb-4 cursor-pointer text-white"
      />
      <router-link to="/signin" class="mb-16">Already have an account? <a class="text-blue-400">Sign in</a></router-link>
    </div>
  </div>
  </form>
  </div>
</template>


<script setup lang="ts">
	import { ref, reactive, onActivated } from 'vue'
	import { useRouter, useRoute } from 'vue-router'
  import {userStore} from '../UserStore'
	import axios from 'axios'

	interface Userdata {
		username: string,
		email: string,
		password: string;
	}

    const route = useRoute()
	const router = useRouter()

  const userstore = userStore()


	let type = ref('password')
	let accountCreated = ref(false)
	const userData: Userdata = reactive({
		username: "",
		email: "",
		password: "",
	});
	const errorMessage= reactive({
		value: false,
		message: ''
	});

	const toogle = () => {
        if (type.value == 'password') { type.value = 'text' } else { type.value = 'password' }
    }

	const signUp = async () => {
        const resp = await userstore.signup(userData.username, userData.email , userData.password)
        if (resp.error) {
            errorMessage.value = true,
            errorMessage.message = resp.error
        }else if(resp.success){
            router.push({ path: 'signin', query: { account: 'created' }})
        }
	}

</script>

// export default {
//   data() {
//     return {
//       userData: {
//         username: "",
//         email: "",
//         password: "",
//       },
//       errorMessage : {
//         value: false,
//         message: ''
//       }
//     };
//   },

//   methods: {
//     signup() {
//         const path = "http://127.0.0.1:5000/api/signup/";
//         axios.post(path, this.userData).then((res) => {
//             if (res.data.error) {
//                 this.errorMessage.value = true
//                 this.errorMessage.message = res.data['error']
//             }
//             else if(res.data.message){
// 				this.$router.push({ path: 'signin', query: { account: 'created' }})
//             }

//         }).catch((error) => {console.log(error)})
//     },
//     resetForm(){
//         this.userData.username = '',
//         this.userData.email = '',
//         this.userData.password = ''
//     }
//   },
// };

// import { reactive } from "vue";

// interface Userdata {
//   email: string;
//   username: string;
//   password: string;
// }
// const userdata: Userdata = reactive({
//   email: "",
//   username: "",
//   password: "",
// });

// const signup = () => {
//   axios
//     .post(path, userdata)
//     .then((res) => {
//       console.log(res.data)
//     })
//     .catch((error) => {
//       console.log(error);
//     });
// };
//