<!-- <template>
	<div
		v-if="actions.length > 0"
		:class="[
			props.view === 'form'
				? 'px-4 pt-4 pb-4 standalone:pb-safe-bottom sm:w-96 bg-white sticky bottom-0 w-full drop-shadow-xl z-40 border-t rounded-t-lg'
				: 'flex w-full flex-row items-center justify-between gap-3 sticky bottom-0 border-t z-[100] p-4',
		]"
	>
		<Button
			v-if="props.view === 'form' || actions.length > 2"
			@click="showTransitions()"
			class="w-full rounded py-5 text-base disabled:bg-gray-700 disabled:text-white"
			variant="solid"
		>
			<template #prefix>
				<FeatherIcon name="chevron-up" class="w-4" />
			</template>
			Actions
		</Button>

		<template v-else>
			<Button
				v-for="action in actions"
				class="w-full py-5"
				:variant="action.variant"
				:theme="action.theme"
				@click="applyWorkflow({ workflowAction: action.text })"
			>
				<template #prefix v-if="action.featherIcon">
					<FeatherIcon :name="action.featherIcon" class="w-4" />
				</template>
				{{ action.text }}
			</Button>
		</template>
	</div>

	<ion-action-sheet
		:buttons="actions"
		:is-open="showActionSheet"
		@didDismiss="applyWorkflow({ event: $event })"
	>
	</ion-action-sheet>
</template>

<script setup>
import { IonActionSheet, modalController } from "@ionic/vue"
import { computed, ref, onMounted } from "vue"
import { FeatherIcon } from "frappe-ui"

const props = defineProps({
	doc: {
		type: Object,
		required: true,
	},
	workflow: {
		type: Object,
		required: false,
	},
	view: {
		type: String,
		default: "form",
		validator: (value) => ["form", "actionSheet"].includes(value),
	},
})

const emit = defineEmits(["workflow-applied"])

let showActionSheet = ref(false)
let actions = ref([])

const getTransitions = async () => {
	const transitions = await props.workflow.getTransitions(props.doc)
	actions.value = transitions.map((transition) => {
		let role = ""
		let theme = "gray"
		let variant = "subtle"
		let icon = ""
		let actionLabel = transition.toLowerCase()

		if (actionLabel.includes("reject") || actionLabel.includes("cancel")) {
			role = "destructive"
			theme = "red"
			variant = "subtle"
			icon = "x"
		} else if (actionLabel.includes("approve")) {
			theme = "green"
			variant = "solid"
			icon = "check"
		}

		return {
			text: transition,
			role: role,
			theme: theme,
			variant: variant,
			featherIcon: icon,
			data: {
				action: transition,
			},
		}
	})
}

const showTransitions = () => {
	if (actions.value?.length > 0) {
		// always add last action for dismissing the modal
		actions.value.push({
			text: "Dismiss",
			role: "cancel",
		})
	}

	showActionSheet.value = true
}

const applyWorkflow = async ({ event = "", workflowAction = "" }) => {
	const action = workflowAction || event.detail.data?.action
	if (action) {
		await props.workflow.applyWorkflow(props.doc, action)
		modalController.dismiss()
		emit("workflow-applied")
	}

	showActionSheet.value = false
}

onMounted(() => getTransitions())
</script>

<style scoped>
ion-action-sheet {
	--button-color: var(--text-gray-500);
}
</style> -->
<template>
	<div
		v-if="actions.length > 0"
		:class="[
			props.view === 'form'
				? 'px-4 pt-4 pb-4 standalone:pb-safe-bottom sm:w-96 bg-white sticky bottom-0 w-full drop-shadow-xl z-40 border-t rounded-t-lg'
				: 'flex w-full flex-row items-center justify-between gap-3 sticky bottom-0 border-t z-[100] p-4',
		]"
	>
		<Button
			v-if="props.view === 'form' || actions.length > 2"
			@click="showTransitions"
			class="w-full rounded py-5 text-base disabled:bg-gray-700 disabled:text-white"
			variant="solid"
		>
			<template #prefix>
				<FeatherIcon name="chevron-up" class="w-4" />
			</template>
			Actions
		</Button>

		<template v-else>
			<Button
				v-for="action in actions"
				:key="action.text"
				class="w-full py-5"
				:variant="action.variant"
				:theme="action.theme"
				@click="applyWorkflow({ workflowAction: action.text })"
			>
				<template #prefix v-if="action.featherIcon">
					<FeatherIcon :name="action.featherIcon" class="w-4" />
				</template>
				{{ action.text }}
			</Button>
		</template>
	</div>

	<ion-action-sheet
		:buttons="actions"
		:is-open="showActionSheet"
		@didDismiss="applyWorkflow({ event: $event })"
	></ion-action-sheet>

	<!-- Remarks Dialog -->
	<!-- <div v-if="showRemarksDialog" class="dialog-overlay">
		<div class="dialog-content">
			<h3>Enter Remarks</h3>
			<textarea v-model="remarks" placeholder="Enter your remarks here..."></textarea>
			<div class="dialog-actions">
				<button @click="submitRemarks">Submit</button>
				<button @click="closeDialog">Cancel</button>
			</div>
		</div>
	</div> -->
	<div v-if="showRemarksDialog" class="dialog-overlay">
  <div class="dialog-content">
    <h3 class="dialog-title">Enter Remarks</h3>
    <textarea
      v-model="remarks"
      placeholder="Enter your remarks here..."
      class="dialog-textarea"
    ></textarea>
    <div class="dialog-actions">
      <button class="btn-primary" @click="submitRemarks">Submit</button>
      <button class="btn-secondary" @click="closeDialog">Cancel</button>
    </div>
  </div>
</div>

</template>

<script setup>
import { IonActionSheet, modalController } from "@ionic/vue";
import { ref, onMounted } from "vue";
import { FeatherIcon , call } from "frappe-ui";

const props = defineProps({
	doc: {
		type: Object,
		required: true,
	},
	workflow: {
		type: Object,
		required: false,
	},
	view: {
		type: String,
		default: "form",
		validator: (value) => ["form", "actionSheet"].includes(value),
	},
});

const emit = defineEmits(["workflow-applied"]);

let showActionSheet = ref(false);
let actions = ref([]);
let showRemarksDialog = ref(false); // State to control the remarks dialog visibility
let remarks = ref(""); // State for the remarks input

const getTransitions = async () => {
	const transitions = await props.workflow.getTransitions(props.doc);
	actions.value = transitions.map((transition) => {
		let role = "";
		let theme = "gray";
		let variant = "subtle";
		let icon = "";
		let actionLabel = transition.toLowerCase();

		if (actionLabel.includes("reject") || actionLabel.includes("cancel")) {
			role = "destructive";
			theme = "red";
			variant = "subtle";
			icon = "x";
		} else if (actionLabel.includes("approve")) {
			theme = "green";
			variant = "solid";
			icon = "check";
		}

		return {
			text: transition,
			role: role,
			theme: theme,
			variant: variant,
			featherIcon: icon,
			data: {
				action: transition,
			},
		};
	});
};

const showTransitions = () => {
	if (actions.value?.length > 0) {
		// Always add last action for dismissing the modal
		actions.value.push({
			text: "Dismiss",
			role: "cancel",
		});
	}
	showActionSheet.value = true;
};

const applyWorkflow = async ({ event = "", workflowAction = "" }) => {
	const action = workflowAction || event.detail.data?.action;
	if (action) {
		if (action.toLowerCase() === "reject") {
			// Open the dialog for remarks if action is 'reject'
			showRemarksDialog.value = true;
			return; // Prevent further execution until remarks are submitted
		}
		
		await props.workflow.applyWorkflow(props.doc, action);
		modalController.dismiss();
		emit("workflow-applied");
	}
	showActionSheet.value = false;
};

const submitRemarks = async () => {
	if (remarks.value) {
		await call('hrms.api.api.set_remark',{remark: remarks.value,dt:props.doc.doctype,dn:props.doc.name});
		await props.workflow.applyWorkflow(props.doc, "Reject", remarks.value); // Pass remarks to the workflow
		emit("workflow-applied");
		remarks.value = ""; 
		closeDialog(); 
		showActionSheet.value = false; 
		modalController.dismiss();
		await getTransitions(); 
	}
};

const closeDialog = () => {
	remarks.value = ""; 
	showRemarksDialog.value = false; // Hide the remarks dialog
};

onMounted(() => getTransitions());
</script>

<style scoped>
ion-action-sheet {
	--button-color: var(--text-gray-500);
}

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog-content {
  background: #ffffff;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  width: 400px;
  max-width: 90%;
}

.dialog-title {
  margin-bottom: 15px;
  font-size: 1.25rem;
  font-weight: bold;
}

.dialog-textarea {
  width: 100%;
  height: 100px;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 10px;
  resize: vertical;
  font-size: 1rem;
  margin-bottom: 15px;
}

.dialog-actions {
  display: flex;
  justify-content: space-between;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #f0f0f0;
  color: #333;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-secondary:hover {
  background-color: #e0e0e0;
}

</style>
