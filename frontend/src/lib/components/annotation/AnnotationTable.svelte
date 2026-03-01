<script lang="ts">
	import { cells, updateCell, addRow, removeRow, COLUMN_LABELS, type CellField } from '$stores/annotation';
	import AnnotationCell from './AnnotationCell.svelte';
	import SearchableSelect from './SearchableSelect.svelte';
	import FeatsEditor from './FeatsEditor.svelte';
	import { UPOS_TAGS, DEPREL_TAGS } from '$utils/ud-tagsets';

	interface Props {
		visibleColumns: string[];
		selectedTokenId?: string | null;
		onTokenSelect?: (tokenId: string) => void;
	}

	let { visibleColumns, selectedTokenId = null, onTokenSelect }: Props = $props();

	const allColumns = ['id_f', 'form', 'lemma', 'upos', 'xpos', 'feats', 'head', 'deprel', 'deps', 'misc'];
	const editableFields: CellField[] = ['form', 'lemma', 'upos', 'xpos', 'feats', 'head', 'deprel', 'deps', 'misc'];

	const columns = $derived(allColumns.filter((c) => visibleColumns.includes(c.toUpperCase()) || c === 'id_f'));

	// FEATS editor state
	let featsEditToken = $state<string | null>(null);
	let featsEditValue = $state('');

	function handleCellChange(tokenId: string, field: CellField, value: string) {
		updateCell(tokenId, field, value);
	}

	function handleSelectChange(tokenId: string, field: CellField, value: string) {
		updateCell(tokenId, field, value);
	}

	function openFeatsEditor(tokenId: string, currentValue: string) {
		featsEditToken = tokenId;
		featsEditValue = currentValue;
	}

	function handleFeatsApply(value: string) {
		if (featsEditToken) {
			updateCell(featsEditToken, 'feats', value);
		}
		featsEditToken = null;
	}

	function isEditable(col: string): col is CellField {
		return editableFields.includes(col as CellField);
	}

	// Set of valid token IDs for HEAD validation
	const validIds = $derived(new Set($cells.map((c) => c.id_f)));

	// Inline validation
	function cellError(cell: typeof $cells[0], col: string): string | null {
		if (col === 'upos' && cell.upos !== '_' && !UPOS_TAGS.includes(cell.upos as any)) {
			return `Invalid UPOS: ${cell.upos}`;
		}
		if (col === 'head') {
			if (cell.head !== '_' && cell.head !== '0') {
				const n = parseInt(cell.head);
				if (isNaN(n) || n < 0) return `Invalid HEAD: ${cell.head}`;
				if (cell.head === cell.id_f) return 'Self-loop: HEAD equals own ID';
				if (!validIds.has(cell.head)) return `HEAD ${cell.head} does not exist`;
			}
		}
		return null;
	}
</script>

<div class="overflow-x-auto">
	<table class="w-full border-collapse text-sm">
		<thead>
			<tr class="bg-muted">
				{#each columns as col}
					<th class="border-r border-b-2 border-border px-2 py-1.5 text-left text-xs font-semibold uppercase tracking-wider">
						{COLUMN_LABELS[col] ?? col}
					</th>
				{/each}
				<th class="w-16 border-b-2 border-border px-2 py-1.5 text-xs font-semibold"></th>
			</tr>
		</thead>
		<tbody>
			{#each $cells as cell, idx (cell.id_f)}
				{@const isMultiword = cell.id_f.includes('-')}
				{@const isSelected = cell.id_f === selectedTokenId}
				{@const isEven = idx % 2 === 0}
				<tr
					class="border-t border-border hover:bg-muted/30 {isMultiword ? 'opacity-70' : ''} {isSelected ? 'bg-blue-50 dark:bg-blue-950/30' : isEven ? 'bg-muted/20' : ''}"
					onclick={() => onTokenSelect?.(cell.id_f)}
				>
					{#each columns as col}
						{@const error = cellError(cell, col)}
						{#if col === 'id_f'}
							<td class="border-r border-border px-2 py-1 text-xs font-mono text-muted-foreground">
								{cell.id_f}
							</td>
						{:else if col === 'upos'}
							<SearchableSelect
								value={cell.upos}
								options={UPOS_TAGS}
								onchange={(v) => handleSelectChange(cell.id_f, 'upos', v)}
								class={error ? 'ring-2 ring-destructive/50' : ''}
							/>
						{:else if col === 'deprel'}
							<SearchableSelect
								value={cell.deprel}
								options={DEPREL_TAGS}
								onchange={(v) => handleSelectChange(cell.id_f, 'deprel', v)}
							/>
						{:else if col === 'feats'}
							<td class="border-r border-border px-1 py-0.5">
								<button
									onclick={() => openFeatsEditor(cell.id_f, cell.feats)}
									class="w-full text-left rounded px-1 py-0.5 text-xs outline-none hover:bg-muted cursor-pointer truncate max-w-[10rem]"
									title={cell.feats}
								>
									{cell.feats === '_' ? '_' : cell.feats}
								</button>
							</td>
						{:else if isEditable(col)}
							<AnnotationCell
								value={cell[col]}
								field={col}
								tokenId={cell.id_f}
								onchange={handleCellChange}
							/>
						{:else}
							<td class="border-r border-border px-2 py-0.5 text-xs">{cell[col as keyof typeof cell]}</td>
						{/if}
						<!-- Validation tooltip -->
						{#if error && col !== 'upos'}
							<td class="p-0 w-0 relative">
								<span class="absolute -left-4 top-0 text-destructive text-[10px]" title={error}>!</span>
							</td>
						{/if}
					{/each}
					<td class="px-1 py-0.5">
						<div class="flex gap-1">
							<button
								onclick={() => addRow(cell.id_f)}
								class="rounded px-1 text-xs text-muted-foreground hover:text-foreground cursor-pointer"
								title="Add row after"
							>+</button>
							{#if !isMultiword}
								<button
									onclick={() => removeRow(cell.id_f)}
									class="rounded px-1 text-xs text-muted-foreground hover:text-destructive cursor-pointer"
									title="Remove row"
								>&times;</button>
							{/if}
						</div>
					</td>
				</tr>
			{/each}
		</tbody>
	</table>
</div>

<!-- FEATS Editor Modal -->
{#if featsEditToken}
	<FeatsEditor
		value={featsEditValue}
		onchange={handleFeatsApply}
		onclose={() => (featsEditToken = null)}
	/>
{/if}
