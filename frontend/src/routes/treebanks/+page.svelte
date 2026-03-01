<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { listTreebanks, createTreebank, deleteTreebank, getLanguages, exportConllu } from '$api/treebanks';
	import { ApiError } from '$api/client';
	import type { TreebankWithProgress } from '$api/types';
	import Button from '$components/common/Button.svelte';
	import Input from '$components/common/Input.svelte';
	import Modal from '$components/common/Modal.svelte';

	let treebanks = $state<TreebankWithProgress[]>([]);
	let languages = $state<Record<string, string>>({});
	let loading = $state(true);

	// Create modal
	let showCreate = $state(false);
	let newTitle = $state('');
	let newLanguage = $state('');
	let createError = $state('');

	// Delete modal
	let showDelete = $state(false);
	let deleteTarget = $state<TreebankWithProgress | null>(null);

	onMount(async () => {
		const [tb, langs] = await Promise.all([listTreebanks(), getLanguages()]);
		treebanks = tb;
		languages = langs;
		loading = false;
	});

	async function handleCreate(e: SubmitEvent) {
		e.preventDefault();
		createError = '';
		try {
			await createTreebank(newTitle, newLanguage);
			treebanks = await listTreebanks();
			showCreate = false;
			newTitle = '';
			newLanguage = '';
		} catch (err) {
			createError = err instanceof ApiError ? err.detail : 'Failed to create treebank';
		}
	}

	async function handleDelete() {
		if (!deleteTarget) return;
		await deleteTreebank(deleteTarget.id);
		treebanks = await listTreebanks();
		showDelete = false;
		deleteTarget = null;
	}

	function confirmDelete(tb: TreebankWithProgress) {
		deleteTarget = tb;
		showDelete = true;
	}
</script>

<div class="mx-auto max-w-7xl px-4 py-8">
	<div class="mb-6 flex items-center justify-between">
		<h1 class="text-2xl font-bold">Treebanks</h1>
		<Button onclick={() => (showCreate = true)}>New treebank</Button>
	</div>

	{#if loading}
		<p class="text-muted-foreground">Loading...</p>
	{:else if treebanks.length === 0}
		<div class="rounded-lg border border-dashed border-border py-12 text-center">
			<p class="text-muted-foreground">No treebanks yet.</p>
			<Button variant="outline" class="mt-3" onclick={() => (showCreate = true)}>Create your first treebank</Button>
		</div>
	{:else}
		<div class="overflow-hidden rounded-lg border border-border">
			<table class="w-full text-sm">
				<thead class="bg-muted text-left">
					<tr>
						<th class="px-4 py-3 font-medium">Title</th>
						<th class="px-4 py-3 font-medium">Language</th>
						<th class="px-4 py-3 font-medium">Sentences</th>
						<th class="px-4 py-3 font-medium">Annotations</th>
						<th class="px-4 py-3 font-medium">Progress</th>
						<th class="px-4 py-3 font-medium">Actions</th>
					</tr>
				</thead>
				<tbody>
					{#each treebanks as tb}
						{@const pct = tb.sentence_count > 0 ? Math.round((tb.complete_count / tb.sentence_count) * 100) : 0}
						<tr class="border-t border-border hover:bg-muted/50">
							<td class="px-4 py-3">
								<a href="/treebanks/{tb.id}" class="font-medium text-primary hover:underline">{tb.title}</a>
							</td>
							<td class="px-4 py-3 text-muted-foreground">{tb.language}</td>
							<td class="px-4 py-3">{tb.sentence_count}</td>
							<td class="px-4 py-3">{tb.annotation_count}</td>
							<td class="px-4 py-3">
								<div class="flex items-center gap-2">
									<div class="h-2 w-20 overflow-hidden rounded-full bg-muted">
										<div class="h-full bg-primary transition-all" style="width: {pct}%"></div>
									</div>
									<span class="text-xs text-muted-foreground">{pct}%</span>
								</div>
							</td>
							<td class="px-4 py-3">
								<div class="flex gap-2">
									<a
										href={exportConllu(tb.id)}
										download
										class="text-xs text-muted-foreground hover:text-foreground"
									>
										Export
									</a>
									<button
										onclick={() => confirmDelete(tb)}
										class="text-xs text-destructive hover:text-destructive/80 cursor-pointer"
									>
										Delete
									</button>
								</div>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	{/if}
</div>

<!-- Create modal -->
<Modal open={showCreate} title="Create treebank" onclose={() => (showCreate = false)}>
	{#if createError}
		<div class="mb-3 rounded-md bg-destructive/10 p-3 text-sm text-destructive">{createError}</div>
	{/if}
	<form onsubmit={handleCreate} class="space-y-4">
		<div class="space-y-2">
			<label for="tb-title" class="text-sm font-medium">Title</label>
			<Input id="tb-title" bind:value={newTitle} required placeholder="e.g. AMGIC" />
		</div>
		<div class="space-y-2">
			<label for="tb-lang" class="text-sm font-medium">Language</label>
			<select
				id="tb-lang"
				bind:value={newLanguage}
				required
				class="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
			>
				<option value="">Select language</option>
				{#each Object.entries(languages) as [name, code]}
					<option value={code}>{name} ({code})</option>
				{/each}
			</select>
		</div>
		<div class="flex justify-end gap-2">
			<Button variant="ghost" onclick={() => (showCreate = false)}>Cancel</Button>
			<Button type="submit">Create</Button>
		</div>
	</form>
</Modal>

<!-- Delete confirmation -->
<Modal open={showDelete} title="Delete treebank" onclose={() => (showDelete = false)}>
	<p class="text-sm">
		Are you sure you want to delete <strong>{deleteTarget?.title}</strong>? This will remove all sentences and annotations. This action cannot be undone.
	</p>
	{#snippet actions()}
		<Button variant="ghost" onclick={() => (showDelete = false)}>Cancel</Button>
		<Button variant="destructive" onclick={handleDelete}>Delete</Button>
	{/snippet}
</Modal>
