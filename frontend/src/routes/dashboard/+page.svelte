<script lang="ts">
	import { onMount } from 'svelte';
	import { user } from '$stores/auth';
	import { listTreebanks } from '$api/treebanks';
	import { getMyAnnotations } from '$api/annotations';
	import type { TreebankWithProgress, AnnotationRead } from '$api/types';

	let treebanks = $state<TreebankWithProgress[]>([]);
	let recentAnnotations = $state<AnnotationRead[]>([]);
	let loading = $state(true);

	const statusLabels = ['New', 'Draft', 'Complete'];

	onMount(async () => {
		const [tb, ann] = await Promise.all([listTreebanks(), getMyAnnotations()]);
		treebanks = tb;
		recentAnnotations = ann.slice(0, 5);
		loading = false;
	});

	function totalSentences() {
		return treebanks.reduce((s, t) => s + t.sentence_count, 0);
	}
</script>

<div class="mx-auto max-w-7xl px-4 py-8">
	<h1 class="mb-6 text-2xl font-bold">Welcome, {$user?.first_name || $user?.username}</h1>

	{#if loading}
		<p class="text-muted-foreground">Loading...</p>
	{:else}
		<div class="mb-8 grid gap-4 sm:grid-cols-3">
			<div class="rounded-lg border border-border p-5">
				<p class="text-sm text-muted-foreground">Treebanks</p>
				<p class="text-3xl font-bold">{treebanks.length}</p>
			</div>
			<div class="rounded-lg border border-border p-5">
				<p class="text-sm text-muted-foreground">Total sentences</p>
				<p class="text-3xl font-bold">{totalSentences()}</p>
			</div>
			<div class="rounded-lg border border-border p-5">
				<p class="text-sm text-muted-foreground">My annotations</p>
				<p class="text-3xl font-bold">{recentAnnotations.length}</p>
			</div>
		</div>

		{#if treebanks.length > 0}
			<section class="mb-8">
				<h2 class="mb-3 text-lg font-semibold">Treebanks</h2>
				<div class="overflow-hidden rounded-lg border border-border">
					<table class="w-full text-sm">
						<thead class="bg-muted text-left">
							<tr>
								<th class="px-4 py-2 font-medium">Title</th>
								<th class="px-4 py-2 font-medium">Language</th>
								<th class="px-4 py-2 font-medium">Sentences</th>
								<th class="px-4 py-2 font-medium">Progress</th>
							</tr>
						</thead>
						<tbody>
							{#each treebanks as tb}
								{@const pct = tb.sentence_count > 0 ? Math.round((tb.complete_count / tb.sentence_count) * 100) : 0}
								<tr class="border-t border-border hover:bg-muted/50">
									<td class="px-4 py-2">
										<a href="/treebanks/{tb.id}" class="text-primary hover:underline">{tb.title}</a>
									</td>
									<td class="px-4 py-2 text-muted-foreground">{tb.language}</td>
									<td class="px-4 py-2">{tb.sentence_count}</td>
									<td class="px-4 py-2">
										<div class="flex items-center gap-2">
											<div class="h-2 w-24 overflow-hidden rounded-full bg-muted">
												<div class="h-full bg-primary transition-all" style="width: {pct}%"></div>
											</div>
											<span class="text-xs text-muted-foreground">{pct}%</span>
										</div>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			</section>
		{/if}

		{#if recentAnnotations.length > 0}
			<section>
				<h2 class="mb-3 text-lg font-semibold">Recent annotations</h2>
				<div class="space-y-2">
					{#each recentAnnotations as ann}
						<div class="flex items-center justify-between rounded-lg border border-border px-4 py-3">
							<div>
								<span class="text-sm font-medium">Sentence #{ann.sentence_id}</span>
								<span class="ml-2 rounded-full bg-muted px-2 py-0.5 text-xs text-muted-foreground">
									{statusLabels[ann.status]}
								</span>
							</div>
							<a href="/annotations/mine" class="text-sm text-primary hover:underline">View</a>
						</div>
					{/each}
				</div>
			</section>
		{/if}
	{/if}
</div>
