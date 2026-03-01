<script lang="ts">
	import { STATUS_CONFIG } from '$utils/status';

	interface Props {
		status: number;
	}

	let { status }: Props = $props();

	const config = $derived(STATUS_CONFIG[status] ?? STATUS_CONFIG[0]);
</script>

<span class="inline-flex items-center gap-1.5 rounded-full px-2 py-0.5 text-xs font-medium {config.color}">
	<span class="h-1.5 w-1.5 rounded-full {config.dot}"></span>
	{config.label}
</span>
