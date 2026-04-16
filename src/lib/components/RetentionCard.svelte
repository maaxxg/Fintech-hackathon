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

<div class="bg-white border border-blue-100 rounded-none p-3">
	<div class="flex justify-between items-start mb-2 gap-2">
		<h4 class="text-[11px] font-bold text-blue-950 uppercase tracking-widest m-0 leading-tight">{method.title}</h4>
		<span
			class="text-[9px] font-bold uppercase tracking-widest px-1.5 py-0.5 rounded-none border {pClass} whitespace-nowrap"
		>
			{method.priority}
		</span>
	</div>
	<p class="text-[10px] text-blue-900/70 leading-relaxed m-0 uppercase tracking-widest font-bold">{method.description}</p>
</div>
