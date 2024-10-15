<template>
	<ion-tab-bar slot="bottom" class="shadow-md sm:w-96 py-2 pb-2 standalone:pb-safe-bottom bg-white text-teal-600">
		<ion-tab-button v-for="item in tabItems" :key="item.title" :tab="item.title" :href="item.route"
			class="relative text-teal-600 bg-white text-xs space-y-1.5 transition active:scale-95">
			<div :class="[
				'absolute inset-0 rounded-full transition-all duration-300 ease-in-out',
				route.path === item.route
					? 'bg-teal-100 scale-100 opacity-100'
					: 'bg-transparent scale-50 opacity-0'
			]"></div>
			<div class="relative z-10 flex flex-col items-center justify-center">
				<component :is="item.icon" :class="[
					'h-5 w-5 transition-colors duration-300',
					route.path === item.route ? 'text-teal-700' : 'text-teal-600'
				]" />
				<div :class="[
					'transition-colors duration-300',
					route.path === item.route ? 'font-semibold text-teal-700' : 'font-normal text-teal-600'
				]">
					{{ item.title }}
				</div>
			</div>
			<div v-if="route.path === item.route"
				class="absolute bottom-0 left-1/2 w-1 h-1 bg-teal-700 rounded-full transform -translate-x-1/2 transition-all duration-300">
			</div>
		</ion-tab-button>
	</ion-tab-bar>
</template>

<script setup>
import { useRoute } from "vue-router"

import { IonTabBar, IonTabButton, IonLabel } from "@ionic/vue"

import HomeIcon from "@/components/icons/HomeIcon.vue"
import LeaveIcon from "@/components/icons/LeaveIcon.vue"
import ExpenseIcon from "@/components/icons/ExpenseIcon.vue"
import SalaryIcon from "@/components/icons/SalaryIcon.vue"
import TravelIcon from "@/components/icons/Travelcon.vue"
// import TravelIocn from "@components/icons/TravelIocn.vue"


const route = useRoute()

const tabItems = [
	{
		icon: HomeIcon,
		title: "Home",
		route: "/home",
	},
	{
		icon: LeaveIcon,
		title: "Leaves",
		route: "/dashboard/leaves",
	},
	{
		icon: ExpenseIcon,
		title: "Expenses",
		route: "/dashboard/expense-claims",
	},
	// {
	// 	icon: TravelIcon,
	// 	title: "Travel",
	// 	route: "/dashboard/travel-claims",
	// },
	{
		icon: SalaryIcon,
		title: "Salary",
		route: "/dashboard/salary-slips",
	},
]
</script>
