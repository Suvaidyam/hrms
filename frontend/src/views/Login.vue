<template>
	<ion-page>
	  <ion-content class="ion-padding">
		<div class="flex min-h-screen w-full flex-col justify-center bg-[#e9f7f4fd] py-12 px-4 sm:px-6 lg:px-8">
		  <div class="sm:mx-auto sm:w-full sm:max-w-md">
			<div class="bg-white py-8 px-4 shadow rounded-lg sm:px-10">
			  <div class="flex flex-col items-center mb-6">
				<FrappeHRLogo class="h-12 w-12 text-blue-900" />
				<h2 class="mt-4 text-2xl sm:text-3xl font-extrabold text-gray-900 text-center">Login to RySS HR</h2>
			  </div>
			  <form class="space-y-6" @submit.prevent="submit">
				<div>
				  <label for="email" class="block text-sm font-medium text-gray-900">Email</label>
				  <div class="mt-1">
					<Input
					  id="email"
					  v-model="email"
					  :type="email !== 'Administrator' ? 'email' : 'text'"
					  autocomplete="username"
					  placeholder="johndoe@mail.com"
					  class="appearance-none block w-full  h-9 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none  sm:text-sm"
					  required
					/>
				  </div>
				</div>
				<div>
				  <label for="password" class="block text-sm font-medium text-gray-900">Password</label>
				  <div class="mt-1">
					<Input
					  id="password"
					  v-model="password"
					  type="password"
					  autocomplete="current-password"
					  placeholder="••••••"
					  class="appearance-none block w-full h-9  border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none  sm:text-sm"
					  required
					/>
				  </div>
				</div>
				<ErrorMessage :message="errorMessage" class="mt-2 text-sm text-red-900" />
				<div>
				  <Button
					:loading="session.login.loading"
					type="submit"
					class="w-full flex justify-center h-9  border border-transparent rounded-md shadow-sm text-sm font-medium text-white !bg-blue-800 !hover:bg-blue-900 focus:outline-none focus:ring-2 focus:ring-offset-2  transition duration-150 ease-in-out"
				  >
					Login
				  </Button>
				</div>
			  </form>
			</div>
		  </div>
		</div>
  
		<Dialog v-model="resetPassword.showDialog">
		  <template #body-title>
			<h2 class="text-lg font-bold text-gray-900">Reset Password</h2>
		  </template>
		  <template #body-content>
			<p class="text-sm text-gray-500">Your password has expired. Please reset your password to continue</p>
		  </template>
		  <template #actions>
			<a
			  :href="resetPassword.link"
			  target="_blank"
			  class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-900 hover:bg-blue-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
			>
			  Go to Reset Password page
			</a>
		  </template>
		</Dialog>
  
		<Dialog v-model="otp.showDialog">
		  <template #body-title>
			<h2 class="text-lg font-bold text-gray-900">OTP Verification</h2>
		  </template>
		  <template #body-content>
			<p v-if="otp.verification.prompt" class="mb-4 text-sm text-gray-500">
			  {{ otp.verification.prompt }}
			</p>
			<form class="space-y-4" @submit.prevent="submit">
			  <div>
				<label for="otp" class="block text-sm font-medium text-gray-900">OTP Code</label>
				<Input
				  id="otp"
				  v-model="otp.code"
				  type="text"
				  autocomplete="one-time-code"
				  placeholder="000000"
				  class="appearance-none block w-full  border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none  sm:text-sm"
				  required
				/>
			  </div>
			  <ErrorMessage :message="errorMessage" class="mt-2 text-sm text-red-900" />
			  <Button
				:loading="session.otp.loading"
				type="submit"
				class="w-full flex justify-center  border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-900 hover:bg-blue-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-150 ease-in-out"
			  >
				Verify
			  </Button>
			</form>
		  </template>
		</Dialog>
	  </ion-content>
	</ion-page>
  </template>
  
  <script setup>
  import { IonPage, IonContent } from "@ionic/vue"
  import { inject, reactive, ref } from "vue"
  import { Input, Button, ErrorMessage, Dialog } from "frappe-ui"
  import FrappeHRLogo from "@/components/icons/FrappeHRLogo.vue"
  
  const email = ref(null)
  const password = ref(null)
  const errorMessage = ref("")
  
  const resetPassword = reactive({
	showDialog: false,
	link: "",
  })
  
  const otp = reactive({
	showDialog: false,
	tmp_id: "",
	code: "",
	verification: {},
  })
  
  const session = inject("$session")
  
  async function submit(e) {
	try {
	  let response
	  if (otp.showDialog) {
		response = await session.otp(otp.tmp_id, otp.code)
	  } else {
		response = await session.login(email.value, password.value)
	  }
  
	  if (response.message === "Password Reset") {
		resetPassword.showDialog = true
		resetPassword.link = response.redirect_to
	  } else {
		resetPassword.showDialog = false
		resetPassword.link = ""
	  }
  
	  if (response.verification) {
		if (response.verification.setup) {
		  otp.showDialog = true
		  otp.tmp_id = response.tmp_id
		  otp.verification = response.verification
		} else {
		  window.open("/login?redirect-to=" + encodeURIComponent(window.location.pathname), "_blank")
		}
	  }
	} catch (error) {
	  errorMessage.value = error.messages.join("\n")
	}
  }
  </script>