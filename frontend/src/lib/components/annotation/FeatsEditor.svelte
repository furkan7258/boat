<script lang="ts">
	import { FEATURES } from '$utils/ud-tagsets';
	import Button from '$components/common/Button.svelte';

	interface Props {
		value: string;
		onchange: (value: string) => void;
		onclose: () => void;
	}

	let { value, onchange, onclose }: Props = $props();

	// Parse initial FEATS string into a map
	function parseFeats(raw: string): Map<string, string> {
		const m = new Map<string, string>();
		if (raw === '_' || !raw) return m;
		for (const pair of raw.split('|')) {
			const [k, v] = pair.split('=');
			if (k && v) m.set(k, v);
		}
		return m;
	}

	let feats = $state(parseFeats(value));
	const featureKeys = Object.keys(FEATURES);

	function setFeat(key: string, val: string) {
		const next = new Map(feats);
		if (val === '') {
			next.delete(key);
		} else {
			next.set(key, val);
		}
		feats = next;
	}

	function apply() {
		if (feats.size === 0) {
			onchange('_');
		} else {
			// Sort features alphabetically by key (UD convention)
			const sorted = [...feats.entries()].sort((a, b) => a[0].localeCompare(b[0]));
			onchange(sorted.map(([k, v]) => `${k}=${v}`).join('|'));
		}
		onclose();
	}

	function clear() {
		feats = new Map();
	}
</script>

<div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50" role="dialog" aria-modal="true" aria-label="Edit features">
	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<!-- svelte-ignore a11y_click_events_have_key_events -->
	<div class="w-full max-w-md rounded-lg bg-background p-4 shadow-lg" onclick={(e) => e.stopPropagation()}>
		<div class="mb-3 flex items-center justify-between">
			<h3 class="text-sm font-semibold">Edit Features</h3>
			<div class="flex gap-2">
				<button onclick={clear} class="text-xs text-muted-foreground hover:text-foreground cursor-pointer">Clear all</button>
				<button onclick={onclose} class="text-muted-foreground hover:text-foreground cursor-pointer">&times;</button>
			</div>
		</div>

		<div class="grid grid-cols-2 gap-2 max-h-80 overflow-auto">
			{#each featureKeys as key}
				{@const currentVal = feats.get(key) ?? ''}
				<div class="flex items-center gap-1.5">
					<label class="text-xs font-medium w-24 text-right text-muted-foreground shrink-0">{key}</label>
					<select
						value={currentVal}
						onchange={(e) => setFeat(key, (e.target as HTMLSelectElement).value)}
						class="flex-1 h-7 rounded border border-input bg-background px-1 text-xs focus-visible:ring-2 focus-visible:ring-ring {currentVal ? 'text-foreground' : 'text-muted-foreground'}"
					>
						<option value="">--</option>
						{#each FEATURES[key] as val}
							<option value={val}>{val}</option>
						{/each}
					</select>
				</div>
			{/each}
		</div>

		<!-- Current string preview -->
		<div class="mt-3 rounded bg-muted px-2 py-1">
			<code class="text-xs">
				{feats.size === 0 ? '_' : [...feats.entries()].sort((a, b) => a[0].localeCompare(b[0])).map(([k, v]) => `${k}=${v}`).join('|')}
			</code>
		</div>

		<div class="mt-3 flex justify-end gap-2">
			<Button variant="ghost" size="sm" onclick={onclose}>Cancel</Button>
			<Button size="sm" onclick={apply}>Apply</Button>
		</div>
	</div>
</div>
