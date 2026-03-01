<script lang="ts">
	import { onMount } from 'svelte';
	import { getMyAnnotations } from '$api/annotations';
	import type { AnnotationDetail } from '$api/types';
	import Button from '$components/common/Button.svelte';

	const statusLabels = ['New', 'Draft', 'Complete'];
	const statusColors = ['bg-muted', 'bg-warning/10 text-warning', 'bg-success/10 text-success'];

	let annotations = $state<AnnotationDetail[]>([]);
	let loading = $state(true);
	let filterStatus = $state<number | undefined>(undefined);

	onMount(loadAnnotations);

	async function loadAnnotations() {
		loading = true;
		annotations = await getMyAnnotations(filterStatus);
		loading = false;
	}

	async function setFilter(status: number | undefined) {
		filterStatus = status;
		await loadAnnotations();
	}
</script>

<div class="mx-auto max-w-7xl px-4 py-8">
	<h1 class="mb-6 text-2xl font-bold">My Annotations</h1>

	<!-- Status filter -->
	<div class="mb-4 flex gap-2">
		<button
			onclick={() => setFilter(undefined)}
			class="rounded-full px-3 py-1 text-xs font-medium transition-colors cursor-pointer
				{filterStatus === undefined ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground hover:bg-muted/80'}"
		>
			All
		</button>
		{#each statusLabels as label, i}
			<button
				onclick={() => setFilter(i)}
				class="rounded-full px-3 py-1 text-xs font-medium transition-colors cursor-pointer
					{filterStatus === i ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground hover:bg-muted/80'}"
			>
				{label}
			</button>
		{/each}
	</div>

	{#if loading}
		<p class="text-muted-foreground">Loading...</p>
	{:else if annotations.length === 0}
		<div class="rounded-lg border border-dashed border-border py-12 text-center">
			<p class="text-muted-foreground">No annotations yet.</p>
			<a href="/treebanks" class="mt-2 inline-block text-sm text-primary hover:underline">Browse treebanks</a>
		</div>
	{:else}
		<div class="space-y-2">
			{#each annotations as ann}
				<div class="flex items-center justify-between rounded-lg border border-border px-4 py-3 hover:bg-muted/50">
					<div class="flex items-center gap-3">
						<span class="rounded-full px-2 py-0.5 text-xs font-medium {statusColors[ann.status]}">
							{statusLabels[ann.status]}
						</span>
						<div>
							<p class="text-sm font-medium">{ann.sentence_sent_id}</p>
							<p class="text-xs text-muted-foreground max-w-lg truncate">{ann.sentence_text}</p>
						</div>
					</div>
					<div class="flex items-center gap-3">
						<span class="text-xs text-muted-foreground">{ann.treebank_title}</span>
						<a
							href="/annotate/{ann.treebank_title}/{ann.sentence_id}"
							class="text-sm text-primary hover:underline"
						>
							Edit
						</a>
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>
