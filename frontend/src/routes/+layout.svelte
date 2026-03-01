<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { initialize, isAuthenticated, isLoading } from '$stores/auth';
	import Navbar from '$components/layout/Navbar.svelte';

	let { children } = $props();

	const publicRoutes = ['/login', '/register'];

	onMount(async () => {
		await initialize();
	});

	$effect(() => {
		if ($isLoading) return;
		const path = page.url.pathname;
		if (!$isAuthenticated && !publicRoutes.includes(path)) {
			goto('/login');
		}
	});

	const showNavbar = $derived(
		$isAuthenticated && !page.url.pathname.startsWith('/annotate/')
	);
</script>

<svelte:head>
	<title>BoAT</title>
</svelte:head>

{#if $isLoading}
	<div class="flex h-screen items-center justify-center">
		<div class="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
	</div>
{:else}
	{#if showNavbar}
		<Navbar />
	{/if}
	{@render children()}
{/if}
