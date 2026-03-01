<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { isAuthenticated, isLoading } from '$stores/auth';

	onMount(() => {
		const unsubLoading = isLoading.subscribe((loading) => {
			if (loading) return;
			const unsub = isAuthenticated.subscribe((authed) => {
				goto(authed ? '/dashboard' : '/login');
				unsub();
			});
		});
		return unsubLoading;
	});
</script>
