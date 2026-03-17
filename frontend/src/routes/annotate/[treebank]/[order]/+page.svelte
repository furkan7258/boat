<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { getAnnotationByPosition, updateAnnotation, updateWordlines } from '$api/annotations';
	import { listSentences } from '$api/sentences';
	import { getTreebankByTitle } from '$api/treebanks';
	import { ApiError } from '$api/client';
	import {
		loadAnnotation,
		cells,
		annotationId,
		sentId,
		sentenceText,
		sentenceMetadata,
		status as annotationStatus,
		notes,
		isDirty,
		isSaving,
		getCellsForSave,
		updateCell
	} from '$stores/annotation';
	import { currentColumns, graphPreference } from '$stores/preferences';
	import { appMode } from '$stores/mode';
	import { createShortcutManager } from '$utils/keyboard';
	import { undo, redo } from '$stores/annotation';
	import AnnotationTable from '$components/annotation/AnnotationTable.svelte';
	import AnnotationToolbar from '$components/annotation/AnnotationToolbar.svelte';
	import CommentsPanel from '$components/annotation/CommentsPanel.svelte';
	import DisplacyGraph from '$components/graph/DisplacyGraph.svelte';
	import Breadcrumb from '$components/layout/Breadcrumb.svelte';
	import Tooltip from '$components/common/Tooltip.svelte';
	import KeyboardShortcutsModal from '$components/common/KeyboardShortcutsModal.svelte';
	import { toast } from '$stores/toast';
	import type { TreebankRead, ValidationProfileRead } from '$api/types';
	import { getValidationProfile } from '$api/validation';

	const treebankSlug = $derived(decodeURIComponent(page.params.treebank!));
	const order = $derived(Number(page.params.order!));
	const offline = $derived($appMode === 'offline');

	let treebank = $state<TreebankRead | null>(null);
	let validationProfile = $state<ValidationProfileRead | null>(null);
	let loading = $state(true);
	let error = $state('');
	let maxOrder = $state(0);
	let visibleColumns = $state<string[]>([]);
	let showComments = $state(false);
	let showGraph = $state(true);

	// Click-to-set-HEAD mode
	let selectedTokenId = $state<string | null>(null);
	let headSelectionMode = $state(false);
	let showShortcuts = $state(false);
	let showHints = $state(false);

	const shortcutManager = createShortcutManager();

	onMount(async () => {
		visibleColumns = $currentColumns;
		showGraph = $graphPreference !== 0;

		// First-use hints
		const dismissed = localStorage.getItem('boat-hints-dismissed');
		if (!dismissed) showHints = true;
		shortcutManager.register([
			{ key: 'p', alt: true, handler: goPrev, description: 'Previous sentence' },
			{ key: 'n', alt: true, handler: goNext, description: 'Next sentence' },
			{ key: 's', alt: true, handler: save, description: 'Save' },
			{ key: 'z', ctrl: true, handler: undo, description: 'Undo' },
			{ key: 'y', ctrl: true, handler: redo, description: 'Redo' },
			{ key: 'd', alt: true, handler: () => (showComments = !showComments), description: 'Toggle discussion' },
			{ key: 'g', alt: true, handler: () => (showGraph = !showGraph), description: 'Toggle graph' },
			{ key: 'h', alt: true, handler: () => (headSelectionMode = !headSelectionMode), description: 'Toggle HEAD selection mode' },
			{ key: 'Escape', handler: () => { headSelectionMode = false; }, description: 'Exit HEAD selection mode' },
			{ key: '?', shift: true, handler: () => (showShortcuts = !showShortcuts), description: 'Show keyboard shortcuts' },
		]);
		shortcutManager.attach();

		// Listen for desktop save events (Ctrl+S from DesktopShortcuts)
		window.addEventListener('boat:save', save);
		window.addEventListener('boat:save-as', saveAs);

		await loadPage();
	});

	onDestroy(() => {
		shortcutManager.detach();
		window.removeEventListener('boat:save', save);
		window.removeEventListener('boat:save-as', saveAs);
	});

	// Update window title in Tauri mode
	$effect(() => {
		if ($appMode !== 'web' && treebank) {
			const dirty = $isDirty ? '[*] ' : '';
			const title = `${dirty}${treebank.title} — Sentence ${order} — BoAT`;
			import('@tauri-apps/api/webviewWindow').then(({ getCurrentWebviewWindow }) => {
				getCurrentWebviewWindow().setTitle(title);
			}).catch(() => {});
		}
	});

	// Warn before closing tab with unsaved changes
	$effect(() => {
		const dirty = $isDirty;
		function beforeUnload(e: BeforeUnloadEvent) {
			if (dirty) {
				e.preventDefault();
			}
		}
		window.addEventListener('beforeunload', beforeUnload);
		return () => window.removeEventListener('beforeunload', beforeUnload);
	});

	async function loadPage() {
		loading = true;
		error = '';
		try {
			const tb = await getTreebankByTitle(treebankSlug);
			treebank = tb;
			const [detail, sents] = await Promise.all([
				getAnnotationByPosition(tb.id, order),
				listSentences(tb.id)
			]);
			loadAnnotation(detail);
			maxOrder = sents.length > 0 ? Math.max(...sents.map((s) => s.order)) : 0;

			// Fetch validation profile (gracefully handle 404)
			try {
				validationProfile = await getValidationProfile(tb.id);
			} catch {
				validationProfile = null;
			}
		} catch (err) {
			error = err instanceof ApiError ? err.detail : 'Failed to load annotation';
		} finally {
			loading = false;
		}
	}

	async function save() {
		if (!$annotationId || !treebank) return;
		isSaving.set(true);
		try {
			await updateWordlines($annotationId, getCellsForSave());
			await updateAnnotation($annotationId, {
				status: $annotationStatus,
				notes: $notes,
			});

			// In offline mode, also persist to disk
			if (offline) {
				const { invoke } = await import('@tauri-apps/api/core');
				await invoke('save_file');
			}

			const detail = await getAnnotationByPosition(treebank.id, order);
			loadAnnotation(detail);
			toast.success('Annotation saved');
		} catch (err) {
			const msg = err instanceof ApiError ? err.detail : 'Failed to save';
			toast.error(msg);
			error = msg;
		} finally {
			isSaving.set(false);
		}
	}

	async function saveAs() {
		if (!treebank) return;
		try {
			const { invoke } = await import('@tauri-apps/api/core');
			await invoke('save_file_as');
			toast.success('File saved');
		} catch (err) {
			if (err !== 'No file selected') {
				toast.error(String(err));
			}
		}
	}

	async function goPrev() {
		if (order <= 1) return;
		if ($isDirty && !confirm('You have unsaved changes. Continue?')) return;
		await goto(`/annotate/${treebankSlug}/${order - 1}`);
		await loadPage();
	}

	async function goNext() {
		if (order >= maxOrder) return;
		if ($isDirty && !confirm('You have unsaved changes. Continue?')) return;
		await goto(`/annotate/${treebankSlug}/${order + 1}`);
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
			<Breadcrumb crumbs={[
				{ label: offline ? 'Home' : 'Treebanks', href: offline ? '/desktop' : '/treebanks' },
				{ label: treebank?.title ?? '...', href: `/treebanks/${treebankSlug}` },
				{ label: `Sentence ${order}` },
			]} />
			<span class="text-sm font-mono text-muted-foreground">#{$sentId}</span>
		</div>
		<div class="flex items-center gap-3 text-sm">
			{#if maxOrder > 0}
				<span class="hidden sm:flex items-center gap-2 text-xs text-muted-foreground">
					Sentence {order} of {maxOrder}
					<span class="inline-block h-1.5 w-24 rounded-full bg-muted overflow-hidden">
						<span class="block h-full rounded-full bg-primary transition-all" style="width: {Math.round((order / maxOrder) * 100)}%"></span>
					</span>
				</span>
			{/if}
			<Tooltip text="Toggle graph (Alt+G)">
				<button
					onclick={() => (showGraph = !showGraph)}
					class="text-muted-foreground hover:text-foreground cursor-pointer {showGraph ? 'text-primary' : ''}"
				>Graph</button>
			</Tooltip>
			<Tooltip text="Click-to-set HEAD (Alt+H)">
				<button
					onclick={() => { headSelectionMode = !headSelectionMode; }}
					class="cursor-pointer {headSelectionMode ? 'text-primary font-medium' : 'text-muted-foreground hover:text-foreground'}"
				>{headSelectionMode ? 'HEAD mode ON' : 'Set HEAD'}</button>
			</Tooltip>
			{#if !offline}
				<Tooltip text="Toggle discussion (Alt+D)">
					<button
						onclick={() => (showComments = !showComments)}
						class="text-muted-foreground hover:text-foreground cursor-pointer {showComments ? 'text-primary' : ''}"
					>Discussion</button>
				</Tooltip>
			{/if}
			<Tooltip text="Keyboard shortcuts (?)">
				<button
					onclick={() => (showShortcuts = true)}
					class="text-muted-foreground hover:text-foreground cursor-pointer rounded border border-border px-1.5 py-0.5 text-xs font-mono"
				>?</button>
			</Tooltip>
			<a href={offline ? '/desktop' : '/dashboard'} class="text-muted-foreground hover:text-foreground">Home</a>
		</div>
	</div>

	{#if headSelectionMode}
		<div class="flex items-center gap-3 border-b border-primary/30 bg-primary/5 px-4 py-2 text-sm">
			<span class="font-medium text-primary">HEAD selection mode</span>
			{#if selectedTokenId}
				<span class="text-muted-foreground">Token <strong class="text-foreground">{selectedTokenId}</strong> selected — click another token in the graph to set as its HEAD</span>
			{:else}
				<span class="text-muted-foreground">Click a token in the table to select it, then click its HEAD in the graph</span>
			{/if}
			<button
				onclick={() => (headSelectionMode = false)}
				class="ml-auto rounded-md border border-border bg-background px-2 py-0.5 text-xs text-muted-foreground hover:text-foreground cursor-pointer"
			>Cancel <kbd class="ml-1 rounded bg-muted px-1 font-mono text-[10px]">Esc</kbd></button>
		</div>
	{/if}

	{#if loading}
		<div class="flex flex-1 items-center justify-center">
			<div class="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
		</div>
	{:else if error}
		<div class="flex flex-1 items-center justify-center">
			<div class="rounded-md bg-destructive/10 p-4 text-destructive">{error}</div>
		</div>
	{:else}
		{#if showHints}
			<div class="flex items-center gap-3 border-b border-border bg-accent px-4 py-2 text-xs text-muted-foreground">
				<span class="font-medium text-foreground">Tips:</span>
				<span>Use <kbd class="rounded bg-muted px-1 font-mono">Alt+H</kbd> for HEAD mode</span>
				<span class="text-border">|</span>
				<span>Toggle columns in the toolbar below</span>
				<span class="text-border">|</span>
				<span>Press <kbd class="rounded bg-muted px-1 font-mono">?</kbd> for all shortcuts</span>
				<button
					onclick={() => { showHints = false; localStorage.setItem('boat-hints-dismissed', '1'); }}
					class="ml-auto cursor-pointer text-muted-foreground hover:text-foreground"
				>&times;</button>
			</div>
		{/if}

		<!-- Sentence text -->
		<div class="border-b border-border bg-muted/30 px-4 py-3">
			<p class="text-sm">{$sentenceText}</p>
			{#if $sentenceMetadata}
				<div class="mt-1 flex flex-wrap gap-2">
					{#each Object.entries($sentenceMetadata) as [key, val]}
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
						{validationProfile}
						onTokenSelect={handleTokenSelect}
					/>
				</div>
			</div>

			<!-- Comments panel (toggleable, web/connected only) -->
			{#if showComments && !offline}
				<div class="w-80 border-l border-border overflow-auto">
					<CommentsPanel />
				</div>
			{/if}
		</div>
	{/if}
</div>

<KeyboardShortcutsModal
	open={showShortcuts}
	shortcuts={shortcutManager.getShortcuts()}
	onclose={() => (showShortcuts = false)}
/>
