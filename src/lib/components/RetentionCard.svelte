<script lang="ts">
	import type { RetentionMethod } from '$lib/types';

	let { method }: { method: RetentionMethod } = $props();

	const priorityClasses: Record<string, string> = {
		high: 'text-red-600 bg-red-50 dark:text-red-400 dark:bg-red-950',
		medium: 'text-amber-600 bg-amber-50 dark:text-amber-400 dark:bg-amber-950',
		low: 'text-emerald-600 bg-emerald-50 dark:text-emerald-400 dark:bg-emerald-950'
	};

	let pClass = $derived(priorityClasses[method.priority] || priorityClasses.medium);
</script>

<div
	class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-5 transition hover:border-indigo-500"
>
	<div class="flex justify-between items-center mb-2 gap-2">
		<h4 class="text-base font-semibold text-gray-900 dark:text-gray-100 m-0">{method.title}</h4>
		<span
			class="text-[0.7rem] font-semibold uppercase tracking-wide px-2.5 py-0.5 rounded-md whitespace-nowrap {pClass}"
		>
			{method.priority}
		</span>
	</div>
	<p class="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">{method.description}</p>
</div>
