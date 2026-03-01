<script lang="ts">
	import { user, logout } from '$stores/auth';
	import { goto } from '$app/navigation';

	async function handleLogout() {
		logout();
		await goto('/login');
	}
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
