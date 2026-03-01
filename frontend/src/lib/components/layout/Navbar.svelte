<script lang="ts">
	import { user, logout } from '$stores/auth';
	import { theme } from '$stores/theme';
	import { goto } from '$app/navigation';

	async function handleLogout() {
		logout();
		await goto('/login');
	}

	let currentTheme = $state<string>('system');
	theme.subscribe((v) => (currentTheme = v));

	function cycleTheme() {
		const order = ['light', 'dark', 'system'] as const;
		type T = (typeof order)[number];
		const idx = order.indexOf(currentTheme as T);
		const next = order[(idx + 1) % order.length];
		theme.set(next);
	}

	const themeIcon = $derived(
		currentTheme === 'light' ? '\u2600' : currentTheme === 'dark' ? '\u263E' : '\u25D0'
	);
</script>

<nav class="border-b border-border bg-background">
	<div class="mx-auto flex h-14 max-w-7xl items-center justify-between px-4">
		<div class="flex items-center gap-6">
			<a href="/dashboard" class="text-lg font-bold tracking-tight">BoAT</a>
			<div class="hidden items-center gap-4 text-sm md:flex">
				<a href="/treebanks" class="text-muted-foreground hover:text-foreground transition-colors">
					Treebanks
				</a>
				<a href="/annotations/mine" class="text-muted-foreground hover:text-foreground transition-colors">
					My Annotations
				</a>
				<a href="/search" class="text-muted-foreground hover:text-foreground transition-colors">
					Search
				</a>
			</div>
		</div>
		<div class="flex items-center gap-4 text-sm">
			<button
				onclick={cycleTheme}
				class="text-muted-foreground hover:text-foreground transition-colors cursor-pointer text-base"
				title="Toggle theme (light/dark/system)"
			>{themeIcon}</button>
			{#if $user}
				<a href="/preferences" class="text-muted-foreground hover:text-foreground transition-colors">
					{$user.username}
				</a>
				<button
					onclick={handleLogout}
					class="text-muted-foreground hover:text-foreground transition-colors cursor-pointer"
				>
					Logout
				</button>
			{/if}
		</div>
	</div>
</nav>
