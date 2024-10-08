<template>
	<BaseLayout pageTitle="Travel Claims">
		<template #body>
			<div class="flex flex-col mt-7 mb-7 p-4 gap-7 ">
				<TravelClaimSummary />
				<div class="w-full ">
					<router-link
						:to="{ name: 'TravelClaimFormView' }"
						v-slot="{ navigate }"
					>
						<Button
							@click="navigate"
							variant=""
							class="w-full py-5 text-base bg-blue-900 text-white "
						>
							Request a Travel 
						</Button>
					</router-link>
				</div>

				<div>
					<div class="text-lg text-gray-800 font-bold">Recent Travel Request</div>
					<RequestList
						:component="markRaw(TravelClaimItem)"
						:items="myClaims.data"
						:addListButton="true"
						listButtonRoute="TravelClaimListView"
					/>
				</div>
				<!-- {{ myClaims }} -->
			</div>
		</template>
	</BaseLayout>
</template>

<script setup>
import { markRaw } from "vue"

import BaseLayout from "@/components/BaseLayout.vue"
import TravelClaimSummary from "../../components/TravelClaimSummary.vue"
import RequestList from "@/components/RequestList.vue"
import TravelClaimItem from "../../components/TravelClaimItem.vue"
import { myClaims } from "../../data/travel_claims"
</script>
