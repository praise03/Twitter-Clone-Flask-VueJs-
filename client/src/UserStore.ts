import { defineStore } from "pinia";
import axios from 'axios'
interface Userdata {
    id: number|null,
    email: string|null,
    username: string|null,
    token: string |null
}

interface Response {
    error?: string,
    success?: string
}

export const userStore = defineStore({
    id: 'user',
    state: () => ({
        userdata: <Userdata>{}

        }),
    persist : true,
    actions: {
        async signup(username:string, email:string, password:string){
            const userData = {
                'username': username,
                'email': email,
                'password': password
            }
            let response = <Response>{}
            const path = "http://127.0.0.1:5000/api/signup/";
            response = await axios.post(path, userData).then( (res) => { 
                if(res.data.error){
                    return {error: res.data['error']}
                }
                else if (res.data.message){
                    return { success: res.data.message}
                }
            }).catch( (error) => { console.log(error) } )
            return response
        },

        async signin(usernameOrEmail:string, password:string){
            const userData = {
                'usernameOrEmail': usernameOrEmail,
                'password': password
            } 
            let response = <Response>{}
            const path = "http://127.0.0.1:5000/api/signin/";
            response = await axios.post(path, userData).then((res) => {
                if (res.data.error) {
                    return { error: res.data['error'] } 
                }
                else if(res.data.message){
                    const token = res.data.token
                    const user = res.data.user

                    this.userdata.id = user.id,
                    this.userdata.email =user.email,
                    this.userdata.username = user.username,
                    this.userdata.token = token
                    
                    return {success : res.data.message }
                }
            }).catch((error) => {return error})
            return response
        },

        signOut(){
            this.userdata.id = null,
            this.userdata.email =null,
            this.userdata.username = null,
            this.userdata.token = null
        },

        async generateToken() {
            const path = "http://127.0.0.1:5000/api/token/generate";
            const res = await axios.post(path, {'user_id': this.userdata.id});
            this.userdata.token = res.data.token
        },

        async validateToken(){
            const path = "http://127.0.0.1:5000/api/token/validate";
            const res = await axios.post(path, {'user_id': this.userdata.id, 'token': this.userdata.token});
            if (res.data.token) {
                this.userdata.token = res.data.token
            }
        },

        async checkFollowing(current_user:number, user:string, token:string){
            const data = {
              'current_user' : current_user,
              'user' : user,
            }
            const path = 'http://127.0.0.1:5000/api/user/following'
            const res = await axios.post(path, data, {headers: {Authorization: token as string }});
            if(res.data.following){
                return res.data.following
            }
        },

        async follow(current_user:number,  user:string, token:string){
            const data = {
              'current_user' : current_user,
              'user' : user,
            }
            const path = 'http://127.0.0.1:5000/api/user/follow'
            const res = await axios.post(path, data, {headers: {Authorization: token as string }});
            if(res.data.message){
                return res.data.message
            }
        },

        async unfollow(current_user:number,  user:string, token:string){
            const data = {
              'current_user' : current_user,
              'user' : user,
            }
            const path = 'http://127.0.0.1:5000/api/user/unfollow'
            const res = await axios.post(path, data,{headers: {Authorization: token as string }});
            if(res.data.message){
                return res.data.message
            }
        }
    }
})