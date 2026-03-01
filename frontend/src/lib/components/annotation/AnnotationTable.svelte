<script lang="ts">
	import { cells, updateCell, addRow, removeRow, COLUMN_LABELS, type CellField } from '$stores/annotation';
	import AnnotationCell from './AnnotationCell.svelte';

	interface Props {
		visibleColumns: string[];
	}

	let { visibleColumns }: Props = $props();

	const allColumns = ['id_f', 'form', 'lemma', 'upos', 'xpos', 'feats', 'head', 'deprel', 'deps', 'misc'];
	const editableFields: CellField[] = ['form', 'lemma', 'upos', 'xpos', 'feats', 'head', 'deprel', 'deps', 'misc'];

	const columns = $derived(allColumns.filter((c) => visibleColumns.includes(c.toUpperCase()) || c === 'id_f'));

	function handleCellChange(tokenId: string, field: CellField, value: string) {
		updateCell(tokenId, field, value);
	}

	function isEditable(col: string): col is CellField {
		return editableFields.includes(col as CellField);
	}
</script>

<div class="overflow-x-auto">
	<table class="w-full border-collapse text-sm">
		<thead>
			<tr class="bg-muted">
				{#each columns as col}
					<th class="border-r border-border px-2 py-1.5 text-left text-xs font-semibold uppercase tracking-wider">
						{COLUMN_LABELS[col] ?? col}
					</th>
				{/each}
				<th class="w-16 px-2 py-1.5 text-xs font-semibold"></th>
			</tr>
		</thead>
		<tbody>
			{#each $cells as cell (cell.id_f)}
				{@const isMultiword = cell.id_f.includes('-')}
				<tr class="border-t border-border hover:bg-muted/30 {isMultiword ? 'opacity-70' : ''}">
					{#each columns as col}
						{#if col === 'id_f'}
							<td class="border-r border-border px-2 py-0.5 text-xs font-mono text-muted-foreground">
								{cell.id_f}
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
