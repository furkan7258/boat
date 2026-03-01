<script lang="ts">
	import type { DiffToken } from '$api/types';

	interface Props {
		tokens: DiffToken[];
	}

	let { tokens }: Props = $props();

	// Get all annotator usernames from the first token
	const annotators = $derived(
		tokens.length > 0 ? Object.keys(tokens[0].annotations) : []
	);

	const DIFF_FIELDS = ['upos', 'head', 'deprel', 'feats'];
</script>

{#if tokens.length > 0 && annotators.length >= 2}
	<div class="overflow-x-auto">
		<table class="w-full border-collapse text-xs">
			<thead>
				<tr class="bg-muted">
					<th class="border-r border-border px-2 py-1.5 font-semibold">ID</th>
					<th class="border-r border-border px-2 py-1.5 font-semibold">FORM</th>
					{#each DIFF_FIELDS as field}
						{#each annotators as ann}
							<th class="border-r border-border px-2 py-1 font-medium">
								<div class="text-[10px] text-muted-foreground">{ann}</div>
								<div>{field.toUpperCase()}</div>
							</th>
						{/each}
					{/each}
				</tr>
			</thead>
			<tbody>
				{#each tokens as tok}
					{@const hasDisagreement = tok.disagreements.length > 0}
					<tr class="border-t border-border {hasDisagreement ? 'bg-destructive/5' : ''}">
						<td class="border-r border-border px-2 py-1 font-mono text-muted-foreground">{tok.id_f}</td>
						<td class="border-r border-border px-2 py-1 font-medium">{tok.form}</td>
						{#each DIFF_FIELDS as field}
							{@const isDisagreed = tok.disagreements.includes(field)}
							{#each annotators as ann}
								{@const val = tok.annotations[ann]?.[field] ?? '_'}
								<td class="border-r border-border px-2 py-1 {isDisagreed ? 'bg-destructive/10 text-destructive font-semibold' : 'text-muted-foreground'}">
									{val}
								</td>
							{/each}
						{/each}
					</tr>
				{/each}
			</tbody>
		</table>
	</div>

	<!-- Summary -->
	{@const totalTokens = tokens.length}
	{@const disagreedTokens = tokens.filter((t) => t.disagreements.length > 0).length}
	<div class="mt-3 flex items-center gap-4 text-xs text-muted-foreground">
		<span>{totalTokens} tokens</span>
		<span>{disagreedTokens} with disagreements</span>
		<span>Agreement: {totalTokens > 0 ? Math.round(((totalTokens - disagreedTokens) / totalTokens) * 100) : 0}%</span>
	</div>
{:else}
	<p class="text-sm text-muted-foreground">Need at least 2 annotators to show diff.</p>
{/if}
