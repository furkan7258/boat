<script lang="ts">
	import { status, isDirty, canUndo, canRedo, isSaving, undo, redo, resetToInitial, notes } from '$stores/annotation';
	import Button from '$components/common/Button.svelte';

	interface Props {
		visibleColumns: string[];
		oncolumnschange: (cols: string[]) => void;
		onsave: () => void;
		onnext: () => void;
		onprev: () => void;
		onstatuschange: (status: number) => void;
		hasPrev: boolean;
		hasNext: boolean;
	}

	let { visibleColumns = $bindable(), oncolumnschange, onsave, onnext, onprev, onstatuschange, hasPrev, hasNext }: Props = $props();

	const allColumns = ['ID', 'FORM', 'LEMMA', 'UPOS', 'XPOS', 'FEATS', 'HEAD', 'DEPREL', 'DEPS', 'MISC'];
	const statusLabels = ['New', 'Draft', 'Complete'];

	let showNotes = $state(false);

	function toggleColumn(col: string) {
		if (col === 'ID' || col === 'FORM') return; // Always visible
		const next = visibleColumns.includes(col)
			? visibleColumns.filter((c) => c !== col)
			: [...visibleColumns, col];
		oncolumnschange(next);
	}
</script>

<div class="flex flex-col gap-2 rounded-lg border border-border bg-background p-3">
	<!-- Top row: navigation + save -->
	<div class="flex items-center justify-between gap-2">
		<div class="flex items-center gap-2">
			<Button variant="outline" size="sm" onclick={onprev} disabled={!hasPrev}>
				Prev
			</Button>
			<Button variant="outline" size="sm" onclick={onnext} disabled={!hasNext}>
				Next
			</Button>
		</div>

		<div class="flex items-center gap-2">
			<Button variant="ghost" size="sm" onclick={undo} disabled={!$canUndo}>
				Undo
			</Button>
			<Button variant="ghost" size="sm" onclick={redo} disabled={!$canRedo}>
				Redo
			</Button>
			<Button variant="ghost" size="sm" onclick={resetToInitial} disabled={!$isDirty}>
				Reset
			</Button>
		</div>

		<div class="flex items-center gap-3">
			<!-- Status selector -->
			<select
				value={$status}
				onchange={(e) => onstatuschange(Number((e.target as HTMLSelectElement).value))}
				class="h-8 rounded-md border border-input bg-background px-2 text-xs focus-visible:ring-2 focus-visible:ring-ring"
			>
				{#each statusLabels as label, i}
					<option value={i}>{label}</option>
				{/each}
			</select>

			<Button
				size="sm"
				onclick={onsave}
				disabled={$isSaving}
			>
				{$isSaving ? 'Saving...' : $isDirty ? 'Save *' : 'Save'}
			</Button>
		</div>
	</div>

	<!-- Column toggles + notes -->
	<div class="flex items-center justify-between gap-2">
		<div class="flex flex-wrap gap-1">
			{#each allColumns as col}
				{@const active = visibleColumns.includes(col)}
				{@const locked = col === 'ID' || col === 'FORM'}
				<button
					onclick={() => toggleColumn(col)}
					disabled={locked}
					class="rounded-full px-2 py-0.5 text-xs font-medium transition-colors cursor-pointer
						{active ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground'}
						{locked ? 'opacity-60 cursor-default' : 'hover:opacity-80'}"
				>
					{col}
				</button>
			{/each}
		</div>
		<button
			onclick={() => (showNotes = !showNotes)}
			class="text-xs text-muted-foreground hover:text-foreground cursor-pointer"
		>
			{showNotes ? 'Hide notes' : 'Notes'}
		</button>
	</div>

	<!-- Notes area (collapsible) -->
	{#if showNotes}
		<textarea
			bind:value={$notes}
			rows="2"
			placeholder="Annotator notes..."
			class="w-full rounded-md border border-input bg-background px-3 py-2 text-xs focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
		></textarea>
	{/if}
</div>
