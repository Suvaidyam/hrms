const routes = [
	{
		name: "TravelClaimListView",
		path: "/travel-claims",
		component: () => import("@/views/travel_claim/List.vue"),
	},
	{
		name: "TravelClaimFormView",
		path: "/travel-claims/new",
		component: () => import("@/views/travel_claim/Form.vue"),
	},
	{
		name: "TravelClaimDetailView",
		path: "/travel-claims/:id",
		props: true,
		component: () => import("@/views/travel_claim/Form.vue"),
	},
]

export default routes
