<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { getAnnotationByPosition, updateAnnotation, updateWordlines } from '$api/annotations';
	import { listSentences } from '$api/sentences';
	import { getTreebank } from '$api/treebanks';
	import { ApiError } from '$api/client';
	import {
		loadAnnotation,
		cells,
		annotationId,
		sentId,
		sentenceText,
		sentenceComments,
		status as annotationStatus,
		notes,
		isDirty,
		isSaving,
		getCellsForSave,
		updateCell
	} from '$stores/annotation';
	import { currentColumns, graphPreference } from '$stores/preferences';
	import { createShortcutManager } from '$utils/keyboard';
	import { undo, redo } from '$stores/annotation';
	import AnnotationTable from '$components/annotation/AnnotationTable.svelte';
	import AnnotationToolbar from '$components/annotation/AnnotationToolbar.svelte';
	import CommentsPanel from '$components/annotation/CommentsPanel.svelte';
	import DisplacyGraph from '$components/graph/DisplacyGraph.svelte';
	import type { TreebankRead } from '$api/types';

	const treebankId = $derived(Number(page.params.treebank));
	const order = $derived(Number(page.params.order));

	let treebank = $state<TreebankRead | null>(null);
	let loading = $state(true);
	let error = $state('');
	let maxOrder = $state(0);
	let visibleColumns = $state<string[]>([]);
	let showComments = $state(false);
	let showGraph = $state(true);

	// Click-to-set-HEAD mode
	let selectedTokenId = $state<string | null>(null);
	let headSelectionMode = $state(false);

	const shortcutManager = createShortcutManager();

	onMount(async () => {
		visibleColumns = $currentColumns;
		showGraph = $graphPreference !== 0;
		shortcutManager.register([
			{ key: 'p', alt: true, handler: goPrev, description: 'Previous sentence' },
			{ key: 'n', alt: true, handler: goNext, description: 'Next sentence' },
			{ key: 's', alt: true, handler: save, description: 'Save' },
			{ key: 'z', ctrl: true, handler: undo, description: 'Undo' },
			{ key: 'y', ctrl: true, handler: redo, description: 'Redo' },
			{ key: 'd', alt: true, handler: () => (showComments = !showComments), description: 'Toggle discussion' },
			{ key: 'g', alt: true, handler: () => (showGraph = !showGraph), description: 'Toggle graph' },
			{ key: 'h', alt: true, handler: () => (headSelectionMode = !headSelectionMode), description: 'Toggle HEAD selection mode' },
		]);
		shortcutManager.attach();
		await loadPage();
	});

	onDestroy(() => {
		shortcutManager.detach();
	});

	async function loadPage() {
		loading = true;
		error = '';
		try {
			const [detail, tb, sents] = await Promise.all([
				getAnnotationByPosition(treebankId, order),
				getTreebank(treebankId),
				listSentences(treebankId, 0, 1000)
			]);
			loadAnnotation(detail);
			treebank = tb;
			maxOrder = sents.length > 0 ? Math.max(...sents.map((s) => s.order)) : 0;
		} catch (err) {
			error = err instanceof ApiError ? err.detail : 'Failed to load annotation';
		} finally {
			loading = false;
		}
	}

	async function save() {
		if (!$annotationId) return;
		isSaving.set(true);
		try {
			await updateWordlines($annotationId, getCellsForSave());
			await updateAnnotation($annotationId, {
				status: $annotationStatus,
				notes: $notes,
			});
			const detail = await getAnnotationByPosition(treebankId, order);
			loadAnnotation(detail);
		} catch (err) {
			error = err instanceof ApiError ? err.detail : 'Failed to save';
		} finally {
			isSaving.set(false);
		}
	}

	async function goPrev() {
		if (order <= 1) return;
		if ($isDirty && !confirm('You have unsaved changes. Continue?')) return;
		await goto(`/annotate/${treebankId}/${order - 1}`);
		await loadPage();
	}

	async function goNext() {
		if (order >= maxOrder) return;
		if ($isDirty && !confirm('You have unsaved changes. Continue?')) return;
		await goto(`/annotate/${treebankId}/${order + 1}`);
		await loadPage();
	}

	function handleStatusChange(newStatus: number) {
		annotationStatus.set(newStatus);
	}

	function handleColumnsChange(cols: string[]) {
		visibleColumns = cols;
	}

	function handleTokenSelect(tokenId: string) {
		selectedTokenId = tokenId;
	}

	function handleGraphTokenClick(tokenId: string) {
		if (headSelectionMode && selectedTokenId && selectedTokenId !== tokenId) {
			// Set the HEAD of selectedTokenId to tokenId
			updateCell(selectedTokenId, 'head', tokenId);
			headSelectionMode = false;
		} else {
			selectedTokenId = tokenId;
		}
	}
</script>

<div class="flex h-screen flex-col">
	<!-- Header bar -->
	<div class="flex items-center justify-between border-b border-border bg-background px-4 py-2">
		<div class="flex items-center gap-4">
			<a href="/treebanks/{treebankId}" class="text-sm text-muted-foreground hover:text-foreground">&larr; {treebank?.title ?? 'Back'}</a>
			<span class="text-sm font-mono text-muted-foreground">#{$sentId}</span>
		</div>
		<div class="flex items-center gap-3 text-sm">
			<button
				onclick={() => (showGraph = !showGraph)}
				class="text-muted-foreground hover:text-foreground cursor-pointer {showGraph ? 'text-primary' : ''}"
			>Graph</button>
			<button
				onclick={() => { headSelectionMode = !headSelectionMode; }}
				class="cursor-pointer {headSelectionMode ? 'text-primary font-medium' : 'text-muted-foreground hover:text-foreground'}"
				title="Click a token in the table, then click its HEAD in the graph (Alt+H)"
			>{headSelectionMode ? 'HEAD mode ON' : 'Set HEAD'}</button>
			<button
				onclick={() => (showComments = !showComments)}
				class="text-muted-foreground hover:text-foreground cursor-pointer {showComments ? 'text-primary' : ''}"
			>Discussion</button>
			<a href="/dashboard" class="text-muted-foreground hover:text-foreground">Home</a>
		</div>
	</div>

	{#if loading}
		<div class="flex flex-1 items-center justify-center">
			<div class="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
		</div>
	{:else if error}
		<div class="flex flex-1 items-center justify-center">
			<div class="rounded-md bg-destructive/10 p-4 text-destructive">{error}</div>
		</div>
	{:else}
		<!-- Sentence text -->
		<div class="border-b border-border bg-muted/30 px-4 py-3">
			<p class="text-sm">{$sentenceText}</p>
			{#if $sentenceComments}
				<div class="mt-1 flex flex-wrap gap-2">
					{#each Object.entries($sentenceComments) as [key, val]}
						<span class="rounded bg-muted px-2 py-0.5 text-xs text-muted-foreground">
							{key}: {val}
						</span>
					{/each}
				</div>
			{/if}
		</div>

		<!-- Main content -->
		<div class="flex flex-1 overflow-hidden">
			<!-- Annotation editor -->
			<div class="flex flex-1 flex-col overflow-hidden">
				<div class="p-3">
					<AnnotationToolbar
						bind:visibleColumns
						onsave={save}
						onnext={goNext}
						onprev={goPrev}
						onstatuschange={handleStatusChange}
						oncolumnschange={handleColumnsChange}
						hasPrev={order > 1}
						hasNext={order < maxOrder}
					/>
				</div>

				<div class="flex-1 overflow-auto px-3 pb-3">
					<!-- Graph above table (hybrid layout) -->
					{#if showGraph}
						<div class="mb-2 rounded-lg border border-border bg-background p-2">
							<DisplacyGraph
								{visibleColumns}
								{selectedTokenId}
								{headSelectionMode}
								onTokenClick={handleGraphTokenClick}
							/>
						</div>
					{/if}

					<!-- Annotation table -->
					<AnnotationTable
						{visibleColumns}
						{selectedTokenId}
						onTokenSelect={handleTokenSelect}
					/>
				</div>
			</div>

			<!-- Comments panel (toggleable) -->
			{#if showComments}
				<div class="w-80 border-l border-border overflow-auto">
					<CommentsPanel />
				</div>
			{/if}
		</div>
	{/if}
</div>
