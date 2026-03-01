<script lang="ts">
	interface Props {
		open: boolean;
		title: string;
		onclose: () => void;
		children?: import('svelte').Snippet;
		actions?: import('svelte').Snippet;
	}

	let { open = $bindable(), title, onclose, children, actions }: Props = $props();

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Escape') onclose();
	}

	function handleBackdrop() {
		onclose();
	}
</script>

{#if open}
	<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
	<div
		class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
		role="dialog"
		aria-modal="true"
		aria-label={title}
		tabindex="-1"
		onkeydown={handleKeydown}
		onclick={handleBackdrop}
	>
		<!-- svelte-ignore a11y_no_static_element_interactions -->
		<div
			class="w-full max-w-lg rounded-lg bg-background p-6 shadow-lg"
			onclick={(e) => e.stopPropagation()}
			onkeydown={(e) => e.stopPropagation()}
		>
			<div class="mb-4 flex items-center justify-between">
				<h2 class="text-lg font-semibold">{title}</h2>
				<button class="text-muted-foreground hover:text-foreground cursor-pointer" onclick={onclose}>&times;</button>
			</div>
			<div class="mb-4">
				{@render children?.()}
			</div>
			{#if actions}
				<div class="flex justify-end gap-2">
					{@render actions()}
				</div>
			{/if}
		</div>
	</div>
{/if}
