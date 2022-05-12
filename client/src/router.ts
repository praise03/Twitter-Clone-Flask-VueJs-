import { createWebHistory, createRouter } from "vue-router";
import Main from './components/Main.vue'
import SignIn from './components/SignIn.vue'
import SignUp from './components/Signup.vue'
import User from './components/User.vue'
import Tweet from './components/Tweet.vue'
import Replies from './components/Replies.vue'
import ErrorPage from './components/404.vue'

const routes = [
    {
        path: '/:pathMatch(.*)*',
        name: 'ErrorPage',
        component: ErrorPage
    },
    {
        path: '/',
        name: 'Main',
        component: Main
    },
    {
        path: '/signin',
        name: 'SignIn',
        component: SignIn
    },
    {
        path: '/signup',
        name: 'SignUp',
        component: SignUp
    },    
    {
        path: '/user/:username',
        name: 'user',
        component: User
    },
    {
        path: '/tweet/:id',
        name: 'post',
        component: Tweet
    },
    {
        path: '/replies/:id',
        name: 'replies',
        component: Replies
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router