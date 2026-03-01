<script lang="ts">
	import { goto } from '$app/navigation';
	import { register } from '$stores/auth';
	import { ApiError } from '$api/client';
	import Button from '$components/common/Button.svelte';
	import Input from '$components/common/Input.svelte';

	let username = $state('');
	let email = $state('');
	let firstName = $state('');
	let lastName = $state('');
	let password = $state('');
	let password2 = $state('');
	let error = $state('');
	let loading = $state(false);

	async function handleSubmit(e: SubmitEvent) {
		e.preventDefault();
		error = '';
		if (password !== password2) {
			error = 'Passwords do not match';
			return;
		}
		loading = true;
		try {
			await register({
				username,
				email,
				password,
				first_name: firstName,
				last_name: lastName
			});
			await goto('/dashboard');
		} catch (err) {
			error = err instanceof ApiError ? err.detail : 'Registration failed';
		} finally {
			loading = false;
		}
	}
</script>

<div class="flex min-h-screen items-center justify-center bg-muted">
	<div class="w-full max-w-sm space-y-6 rounded-lg bg-background p-8 shadow-lg">
		<div class="text-center">
			<h1 class="text-2xl font-bold">Create account</h1>
			<p class="text-sm text-muted-foreground">Join BoAT to start annotating</p>
		</div>

		{#if error}
			<div class="rounded-md bg-destructive/10 p-3 text-sm text-destructive">{error}</div>
		{/if}

		<form onsubmit={handleSubmit} class="space-y-4">
			<div class="grid grid-cols-2 gap-3">
				<div class="space-y-2">
					<label for="firstName" class="text-sm font-medium">First name</label>
					<Input id="firstName" bind:value={firstName} required />
				</div>
				<div class="space-y-2">
					<label for="lastName" class="text-sm font-medium">Last name</label>
					<Input id="lastName" bind:value={lastName} required />
				</div>
			</div>
			<div class="space-y-2">
				<label for="username" class="text-sm font-medium">Username</label>
				<Input id="username" bind:value={username} required />
			</div>
			<div class="space-y-2">
				<label for="email" class="text-sm font-medium">Email</label>
				<Input id="email" type="email" bind:value={email} required />
			</div>
			<div class="space-y-2">
				<label for="password" class="text-sm font-medium">Password</label>
				<Input id="password" type="password" bind:value={password} required />
			</div>
			<div class="space-y-2">
				<label for="password2" class="text-sm font-medium">Confirm password</label>
				<Input id="password2" type="password" bind:value={password2} required />
			</div>
			<Button type="submit" class="w-full" disabled={loading}>
				{loading ? 'Creating account...' : 'Register'}
			</Button>
		</form>

		<p class="text-center text-sm text-muted-foreground">
			Already have an account?
			<a href="/login" class="text-primary hover:underline">Sign in</a>
		</p>
	</div>
</div>
