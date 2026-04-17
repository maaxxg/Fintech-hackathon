<script lang="ts">
	import type { RetentionMethod } from '$lib/types';

	let { method }: { method: RetentionMethod } = $props();

	const priorityClasses: Record<string, string> = {
		high: 'text-blue-900 bg-blue-100 border-blue-900',
		medium: 'text-blue-700 bg-white border-blue-300',
		low: 'text-blue-500 bg-white border-blue-200'
	};

	let pClass = $derived(priorityClasses[method.priority] || priorityClasses.medium);
</script>

<div class="rounded-none border border-blue-100 bg-white p-3">
	<div class="mb-2 flex items-start justify-between gap-2">
		<h4 class="m-0 text-[11px] leading-tight font-bold tracking-widest text-blue-950 uppercase">
			{method.title}
		</h4>
		<span
			class="rounded-none border px-1.5 py-0.5 text-[9px] font-bold tracking-widest uppercase {pClass} whitespace-nowrap"
		>
			{method.priority}
		</span>
	</div>
	<p class="m-0 text-[10px] leading-relaxed font-bold tracking-widest text-blue-900/70 uppercase">
		{method.description}
	</p>
</div>
