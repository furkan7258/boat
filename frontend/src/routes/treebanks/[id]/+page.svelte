<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { getTreebank, uploadConllu, exportConllu } from '$api/treebanks';
	import { listSentences, createSentence, deleteSentence } from '$api/sentences';
	import { createAnnotation } from '$api/annotations';
	import { ApiError } from '$api/client';
	import type { TreebankRead, SentenceBrief } from '$api/types';
	import Button from '$components/common/Button.svelte';
	import Input from '$components/common/Input.svelte';
	import Modal from '$components/common/Modal.svelte';

	const treebankId = $derived(Number(page.params.id));

	let treebank = $state<TreebankRead | null>(null);
	let sentences = $state<SentenceBrief[]>([]);
	let loading = $state(true);
	let currentPage = $state(0);
	const pageSize = 20;

	// Add sentence
	let showAdd = $state(false);
	let newSentId = $state('');
	let newText = $state('');
	let addError = $state('');

	// Upload
	let showUpload = $state(false);
	let uploadFile = $state<File | null>(null);
	let uploadMsg = $state('');
	let uploadError = $state('');

	// Delete
	let showDelete = $state(false);
	let deleteTarget = $state<SentenceBrief | null>(null);

	onMount(loadData);

	async function loadData() {
		loading = true;
		const [tb, sents] = await Promise.all([
			getTreebank(treebankId),
			listSentences(treebankId, currentPage * pageSize, pageSize)
		]);
		treebank = tb;
		sentences = sents;
		loading = false;
	}

	async function goPage(p: number) {
		currentPage = p;
		sentences = await listSentences(treebankId, currentPage * pageSize, pageSize);
	}

	async function handleAddSentence(e: SubmitEvent) {
		e.preventDefault();
		addError = '';
		try {
			await createSentence(treebankId, newSentId, newText);
			showAdd = false;
			newSentId = '';
			newText = '';
			await loadData();
		} catch (err) {
			addError = err instanceof ApiError ? err.detail : 'Failed to add sentence';
		}
	}

	async function handleUpload(e: SubmitEvent) {
		e.preventDefault();
		uploadError = '';
		uploadMsg = '';
		if (!uploadFile) return;
		try {
			const result = await uploadConllu(treebankId, uploadFile);
			uploadMsg = `Imported ${result.created_sentences} sentences.`;
			uploadFile = null;
			await loadData();
		} catch (err) {
			uploadError = err instanceof ApiError ? err.detail : 'Upload failed';
		}
	}

	async function handleDelete() {
		if (!deleteTarget) return;
		await deleteSentence(deleteTarget.id);
		deleteTarget = null;
		showDelete = false;
		await loadData();
	}

	async function annotate(sentence: SentenceBrief) {
		// Create annotation for current user, then navigate to editor
		try {
			const ann = await createAnnotation(sentence.id);
			window.location.href = `/annotate/${treebankId}/${sentence.order}`;
		} catch (err) {
			// If annotation already exists, navigate anyway
			window.location.href = `/annotate/${treebankId}/${sentence.order}`;
		}
	}

	function onFileChange(e: Event) {
		const input = e.target as HTMLInputElement;
		uploadFile = input.files?.[0] ?? null;
	}
</script>

<div class="mx-auto max-w-7xl px-4 py-8">
	{#if loading}
		<p class="text-muted-foreground">Loading...</p>
	{:else if treebank}
		<div class="mb-6">
			<div class="mb-1 flex items-center gap-3">
				<a href="/treebanks" class="text-sm text-muted-foreground hover:text-foreground">&larr; Treebanks</a>
			</div>
			<div class="flex items-center justify-between">
				<div>
					<h1 class="text-2xl font-bold">{treebank.title}</h1>
					<p class="text-sm text-muted-foreground">{treebank.language}</p>
				</div>
				<div class="flex gap-2">
					<Button variant="outline" onclick={() => (showUpload = true)}>Upload CoNLL-U</Button>
					<Button variant="outline" onclick={() => (showAdd = true)}>Add sentence</Button>
					<a
						href={exportConllu(treebank.id)}
						download
						class="inline-flex h-9 items-center rounded-md border border-input bg-background px-4 text-sm font-medium hover:bg-accent hover:text-accent-foreground"
					>
						Export
					</a>
				</div>
			</div>
		</div>

		{#if sentences.length === 0}
			<div class="rounded-lg border border-dashed border-border py-12 text-center">
				<p class="text-muted-foreground">No sentences yet. Upload a CoNLL-U file or add sentences manually.</p>
			</div>
		{:else}
			<div class="overflow-hidden rounded-lg border border-border">
				<table class="w-full text-sm">
					<thead class="bg-muted text-left">
						<tr>
							<th class="px-4 py-3 font-medium w-16">#</th>
							<th class="px-4 py-3 font-medium w-32">Sent ID</th>
							<th class="px-4 py-3 font-medium">Text</th>
							<th class="px-4 py-3 font-medium w-36">Actions</th>
						</tr>
					</thead>
					<tbody>
						{#each sentences as sent}
							<tr class="border-t border-border hover:bg-muted/50">
								<td class="px-4 py-3 text-muted-foreground">{sent.order}</td>
								<td class="px-4 py-3 font-mono text-xs">{sent.sent_id}</td>
								<td class="px-4 py-3 max-w-xl truncate">{sent.text}</td>
								<td class="px-4 py-3">
									<div class="flex gap-2">
										<button
											onclick={() => annotate(sent)}
											class="text-xs text-primary hover:underline cursor-pointer"
										>
											Annotate
										</button>
										<button
											onclick={() => { deleteTarget = sent; showDelete = true; }}
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

			<!-- Pagination -->
			<div class="mt-4 flex items-center justify-between">
				<Button variant="outline" size="sm" disabled={currentPage === 0} onclick={() => goPage(currentPage - 1)}>
					Previous
				</Button>
				<span class="text-sm text-muted-foreground">Page {currentPage + 1}</span>
				<Button
					variant="outline"
					size="sm"
					disabled={sentences.length < pageSize}
					onclick={() => goPage(currentPage + 1)}
				>
					Next
				</Button>
			</div>
		{/if}
	{/if}
</div>

<!-- Add sentence modal -->
<Modal open={showAdd} title="Add sentence" onclose={() => (showAdd = false)}>
	{#if addError}
		<div class="mb-3 rounded-md bg-destructive/10 p-3 text-sm text-destructive">{addError}</div>
	{/if}
	<form onsubmit={handleAddSentence} class="space-y-4">
		<div class="space-y-2">
			<label for="sent-id" class="text-sm font-medium">Sentence ID</label>
			<Input id="sent-id" bind:value={newSentId} required placeholder="e.g. sent-001" />
		</div>
		<div class="space-y-2">
			<label for="sent-text" class="text-sm font-medium">Text</label>
			<textarea
				id="sent-text"
				bind:value={newText}
				required
				rows="3"
				class="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
				placeholder="Enter sentence text..."
			></textarea>
		</div>
		<div class="flex justify-end gap-2">
			<Button variant="ghost" onclick={() => (showAdd = false)}>Cancel</Button>
			<Button type="submit">Add</Button>
		</div>
	</form>
</Modal>

<!-- Upload modal -->
<Modal open={showUpload} title="Upload CoNLL-U file" onclose={() => { showUpload = false; uploadMsg = ''; uploadError = ''; }}>
	{#if uploadError}
		<div class="mb-3 rounded-md bg-destructive/10 p-3 text-sm text-destructive">{uploadError}</div>
	{/if}
	{#if uploadMsg}
		<div class="mb-3 rounded-md bg-success/10 p-3 text-sm text-success">{uploadMsg}</div>
	{/if}
	<form onsubmit={handleUpload} class="space-y-4">
		<div class="space-y-2">
			<label for="conllu-file" class="text-sm font-medium">CoNLL-U file</label>
			<input
				id="conllu-file"
				type="file"
				accept=".conllu,.conll,.txt"
				onchange={onFileChange}
				class="block w-full text-sm file:mr-4 file:rounded-md file:border-0 file:bg-primary file:px-4 file:py-2 file:text-sm file:font-medium file:text-primary-foreground hover:file:bg-primary/90"
			/>
		</div>
		<div class="flex justify-end gap-2">
			<Button variant="ghost" onclick={() => { showUpload = false; uploadMsg = ''; uploadError = ''; }}>Close</Button>
			<Button type="submit" disabled={!uploadFile}>Upload</Button>
		</div>
	</form>
</Modal>

<!-- Delete confirmation -->
<Modal open={showDelete} title="Delete sentence" onclose={() => (showDelete = false)}>
	<p class="text-sm">
		Are you sure you want to delete sentence <strong>{deleteTarget?.sent_id}</strong>? All annotations will be removed.
	</p>
	{#snippet actions()}
		<Button variant="ghost" onclick={() => (showDelete = false)}>Cancel</Button>
		<Button variant="destructive" onclick={handleDelete}>Delete</Button>
	{/snippet}
</Modal>
