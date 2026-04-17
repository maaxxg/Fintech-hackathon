<script lang="ts">
	import type { RetentionMethod } from '$lib/types';

	let { method }: { method: RetentionMethod } = $props();

	const priorityClasses: Record<string, string> = {
		high: 'text-red-900 bg-red-100 border-red-900',
		medium: 'text-red-700 bg-white border-red-300',
		low: 'text-red-500 bg-white border-red-200'
	};

	let pClass = $derived(priorityClasses[method.priority] || priorityClasses.medium);
</script>

<div class="rounded-none border border-red-100 bg-white p-3">
	<div class="mb-2 flex items-start justify-between gap-2">
		<h4 class="m-0 text-[11px] leading-tight font-bold tracking-widest text-red-950 uppercase">
			{method.title}
		</h4>
		<span
			class="rounded-none border px-1.5 py-0.5 text-[9px] font-bold tracking-widest uppercase {pClass} whitespace-nowrap"
		>
			{method.priority}
		</span>
	</div>
	<p class="m-0 text-[10px] leading-relaxed font-bold tracking-widest text-red-900/70 uppercase">
		{method.description}
	</p>
</div>
