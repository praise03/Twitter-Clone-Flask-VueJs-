import { defineStore } from "pinia";
import axios from 'axios'
import {reactive, ref} from 'vue'


interface Response {
    error?: string,
    success?: string
}

export const postStore = defineStore({
    id: 'post',
    state: () => ({
        modal : reactive({
            hidden: false,
            body: '',
            showSignIn: false
        })
    }),
    actions: {
        async createTweet(body:string, author:number, token:string){
            const tweetData = {
                'body': body,
                'author': author
            }
            const response = await axios.post('http://127.0.0.1:5000/api/tweet/create', tweetData,
                {headers: {Authorization: token as string }})
            return response.data.message as string
            
        },

        async likeTweet(tweet:number, user:number, token:string){
            const Data = {
                'tweet': tweet,
                'user': user
            }
            const response = await axios.post('http://127.0.0.1:5000/api/tweet/like', Data,
                {headers: {Authorization: token as string }})
            return response.data.message as string
        },

        async comment(body:string, author:number, tweet:number, token:string){
            const commentData = {
                'body': body,
                'author': author,
                'tweet': tweet
            }
            const response = await axios.post('http://127.0.0.1:5000/api/tweet/comment', commentData,
                {headers: {Authorization: token as string }})
            return response.data.message as string   
        },

        async likeComment(user:number, comment:number, token:string){
            const commentData = {
                'user': user,
                'comment': comment
            }
            const response = await axios.post('http://127.0.0.1:5000/api/comment/like', commentData,
                {headers: {Authorization: token as string }})
            return response.data.message as string   
        },
    }
})