<script lang="ts">
	import { onMount } from 'svelte';
	import { search, type SearchQuery } from '$api/search';
	import { listTreebanks } from '$api/treebanks';
	import type { SearchResult, SearchResponse, TreebankWithProgress } from '$api/types';
	import Button from '$components/common/Button.svelte';
	import Input from '$components/common/Input.svelte';

	const FIELD_OPTIONS = [
		'sent_id', 'text', 'form', 'lemma', 'upos', 'xpos', 'feats', 'head', 'deprel', 'deps', 'misc'
	];

	interface QueryRow {
		field: string;
		value: string;
	}

	let treebanks = $state<TreebankWithProgress[]>([]);
	let selectedTreebank = $state('');
	let queries = $state<QueryRow[]>([{ field: 'upos', value: '' }]);
	let results = $state<SearchResult[]>([]);
	let total = $state(0);
	let searched = $state(false);
	let loading = $state(false);
	let currentPage = $state(0);
	const pageSize = 20;

	onMount(async () => {
		treebanks = await listTreebanks();
	});

	function addRow() {
		queries = [...queries, { field: 'form', value: '' }];
	}

	function removeRow(index: number) {
		queries = queries.filter((_, i) => i !== index);
	}

	async function handleSearch(e?: SubmitEvent) {
		e?.preventDefault();
		loading = true;
		currentPage = 0;
		const activeQueries: SearchQuery[] = queries
			.filter((q) => q.value.trim())
			.map((q) => ({ field: q.field, value: q.value.trim() }));
		const response = await search(activeQueries, selectedTreebank || undefined, 0, pageSize);
		results = response.results;
		total = response.total;
		searched = true;
		loading = false;
	}

	async function goPage(p: number) {
		currentPage = p;
		loading = true;
		const activeQueries: SearchQuery[] = queries
			.filter((q) => q.value.trim())
			.map((q) => ({ field: q.field, value: q.value.trim() }));
		const response = await search(activeQueries, selectedTreebank || undefined, p * pageSize, pageSize);
		results = response.results;
		total = response.total;
		loading = false;
	}
</script>

<div class="mx-auto max-w-7xl px-4 py-8">
	<h1 class="mb-6 text-2xl font-bold">Search</h1>

	<form onsubmit={handleSearch} class="mb-6 space-y-3">
		<div class="flex gap-3 items-end">
			<div class="space-y-1">
				<label for="tb-select" class="text-xs font-medium text-muted-foreground">Treebank</label>
				<select
					id="tb-select"
					bind:value={selectedTreebank}
					class="flex h-9 rounded-md border border-input bg-background px-3 text-sm focus-visible:ring-2 focus-visible:ring-ring"
				>
					<option value="">All treebanks</option>
					{#each treebanks as tb}
						<option value={tb.title}>{tb.title}</option>
					{/each}
				</select>
			</div>
		</div>

		{#each queries as q, i}
			<div class="flex items-center gap-2">
				<select
					bind:value={q.field}
					class="flex h-9 rounded-md border border-input bg-background px-2 text-sm focus-visible:ring-2 focus-visible:ring-ring"
				>
					{#each FIELD_OPTIONS as opt}
						<option value={opt}>{opt.toUpperCase()}</option>
					{/each}
				</select>
				<Input bind:value={q.value} placeholder="Search value..." class="flex-1" />
				{#if queries.length > 1}
					<button onclick={() => removeRow(i)} class="text-muted-foreground hover:text-destructive cursor-pointer">&times;</button>
				{/if}
			</div>
		{/each}

		<div class="flex gap-2">
			<Button variant="outline" size="sm" onclick={addRow}>+ Add condition</Button>
			<Button type="submit" size="sm" disabled={loading}>
				{loading ? 'Searching...' : 'Search'}
			</Button>
		</div>
	</form>

	{#if searched}
		{#if results.length === 0}
			<p class="text-muted-foreground">No results found.</p>
		{:else}
			<div class="overflow-hidden rounded-lg border border-border">
				<table class="w-full text-sm">
					<thead class="bg-muted text-left">
						<tr>
							<th class="px-3 py-2 font-medium">Sent ID</th>
							<th class="px-3 py-2 font-medium">Text</th>
							<th class="px-3 py-2 font-medium">Treebank</th>
							<th class="px-3 py-2 font-medium">FORM</th>
							<th class="px-3 py-2 font-medium">UPOS</th>
							<th class="px-3 py-2 font-medium">DEPREL</th>
						</tr>
					</thead>
					<tbody>
						{#each results as r}
							<tr class="border-t border-border hover:bg-muted/50">
								<td class="px-3 py-2 font-mono text-xs">{r.sentence_sent_id}</td>
								<td class="px-3 py-2 max-w-xs truncate">{r.sentence_text}</td>
								<td class="px-3 py-2 text-muted-foreground">{r.treebank_title}</td>
								<td class="px-3 py-2 font-medium">{r.form}</td>
								<td class="px-3 py-2">{r.upos}</td>
								<td class="px-3 py-2">{r.deprel}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>

			<div class="mt-4 flex items-center justify-between">
				<Button variant="outline" size="sm" disabled={currentPage === 0} onclick={() => goPage(currentPage - 1)}>
					Previous
				</Button>
				<span class="text-sm text-muted-foreground">
					Showing {currentPage * pageSize + 1}–{currentPage * pageSize + results.length} of {total} results
				</span>
				<Button variant="outline" size="sm" disabled={currentPage * pageSize + results.length >= total} onclick={() => goPage(currentPage + 1)}>
					Next
				</Button>
			</div>
		{/if}
	{/if}
</div>
