<template>
	<div class="flex flex-col bg-white rounded w-full py-6 px-4 border-none">
		<h2 class="text-lg font-bold text-gray-900">
			Hey, {{ employee?.data?.first_name }} 👋
		</h2>
		<div class="font-medium text-sm text-gray-500 mt-1.5" v-if="lastLog">
			Last {{ lastLogType }} was at {{ lastLogTime }}
		</div>
		<Button class="mt-4 mb-1 drop-shadow-sm py-5 text-base" id="open-checkin-modal"
			@click="checkinTimestamp = dayjs().format('YYYY-MM-DD HH:mm:ss')">
			<template #prefix>
				<FeatherIcon :name="nextAction.action === 'IN'
					? 'arrow-right-circle'
					: 'arrow-left-circle'
					" class="w-4" />
			</template>
			{{ nextAction.label }}
		</Button>
	</div>

	<ion-modal ref="modal" trigger="open-checkin-modal" :initial-breakpoint="1" :breakpoints="[0, 1]">
		<div class="h-40 w-full flex flex-col items-center justify-center gap-5 p-4 mb-5">
			<div class="flex flex-col gap-1.5 items-center justify-center">
				<div class="font-bold text-xl">
					{{ dayjs(checkinTimestamp).format("hh:mm:ss a") }}
				</div>
				<div class="font-medium text-gray-500 text-sm">
					{{ dayjs().format("D MMM, YYYY") }}
				</div>
			</div>
                <Button
                    :disabled=loader
                    variant="solid"
                    :class="{'bg-black': loader}"
                    class="w-full py-5 text-sm relative" @click="submitLog(nextAction.action);"
                    >
                    Confirm {{ nextAction.label }}
                    <LoadingIndicator  v-if="loader"  class="absolute top-3 left-[350px] h-4 w-4 "/>
                </Button>
		</div>
	</ion-modal>
</template>

<script setup>
import { createListResource, toast, FeatherIcon } from "frappe-ui"
import { computed, inject, ref, onMounted, onBeforeUnmount } from "vue"
import { IonModal, modalController } from "@ionic/vue"
import { LoadingIndicator } from "frappe-ui";
import { defaults } from "autoprefixer";
const DOCTYPE = "Employee Checkin"
const socket = inject("$socket")
const employee = inject("$employee")
const dayjs = inject("$dayjs")
const checkinTimestamp = ref(null)
const loader = ref(false)

const checkins = createListResource({
	doctype: DOCTYPE,
	fields: [
		"name",
		"employee",
		"employee_name",
		"log_type",
		"time",
		"device_id",
	],
	filters: {
		employee: employee.data.name,
	},
	orderBy: "time desc",
})
checkins.reload()

const lastLog = computed(() => {
	if (checkins.list.loading || !checkins.data) return {}
	return checkins.data[0]
})

const lastLogType = computed(() => {
	return lastLog?.value?.log_type === "IN" ? "check-in" : "check-out"
})
const nextAction = computed(() => {
	return lastLog?.value?.log_type === "IN"
		? { action: "OUT", label: "Check Out" }
		: { action: "IN", label: "Check In" }
})

const lastLogTime = computed(() => {
	const timestamp = lastLog?.value?.time
	const formattedTime = dayjs(timestamp).format("hh:mm a")

	if (dayjs(timestamp).isToday()) return formattedTime
	else if (dayjs(timestamp).isYesterday()) return `${formattedTime} yesterday`
	else if (dayjs(timestamp).isSame(dayjs(), "year"))
		return `${formattedTime} on ${dayjs(timestamp).format("D MMM")}`

	return `${formattedTime} on ${dayjs(timestamp).format("D MMM, YYYY")}`
})


const submitLog = async (logType) => {
	loader.value=true
	const action = logType === "IN" ? "Check-in" : "Check-out";
	let geolocation;
	
	if (navigator.geolocation) {
		try {
			const position = await new Promise((resolve, reject) => {
				navigator.geolocation.getCurrentPosition(resolve, reject, {
					enableHighAccuracy: true// Increase timeout to 10 seconds
				});
			});
			geolocation = `${position.coords.latitude},${position.coords.longitude}`;
		} catch (error) {
			console.error("Error occurred while retrieving geolocation:", error);
			return null;
		}
	} else {
		console.error("Geolocation is not supported by this browser.");
		return null;
	}
	checkins.insert.submit(
		{
			employee: employee.data.name,
			log_type: logType,
			time: checkinTimestamp.value,
			device_id: geolocation
		},
		{
			onSuccess() {
				loader.value=false
				modalController.dismiss()
				toast({
					title: "Success",
					text: `${action} successful!`,
					icon: "check-circle",
					position: "bottom-center",
					iconClasses: "text-green-500",
				})
			},
			onError() {
				loader.value=false
				toast({
					title: "Error",
					text: `${action} failed!`,
					icon: "alert-circle",
					position: "bottom-center",
					iconClasses: "text-red-500",
				})
			},
		}
	)
}

onMounted(() => {
	socket.emit("doctype_subscribe", DOCTYPE)
	socket.on("list_update", (data) => {
		if (data.doctype == DOCTYPE) {
			checkins.reload()
		}
	})
})

onBeforeUnmount(() => {
	socket.emit("doctype_unsubscribe", DOCTYPE)
	socket.off("list_update")
})


</script>
