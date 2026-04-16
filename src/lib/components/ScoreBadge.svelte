<script lang="ts">
	let { label = '', score = 0, type = 'risk' as 'risk' | 'value' } = $props();

	// Risk: high = red (bad), low = green (good)
	// Value: high = green (good), low = red (bad)
	let colorClass = $derived(
		type === 'risk'
			? score >= 70
				? 'text-red-600 bg-red-50 dark:text-red-400 dark:bg-red-950'
				: score >= 40
					? 'text-amber-600 bg-amber-50 dark:text-amber-400 dark:bg-amber-950'
					: 'text-emerald-600 bg-emerald-50 dark:text-emerald-400 dark:bg-emerald-950'
			: score >= 70
				? 'text-emerald-600 bg-emerald-50 dark:text-emerald-400 dark:bg-emerald-950'
				: score >= 40
					? 'text-amber-600 bg-amber-50 dark:text-amber-400 dark:bg-amber-950'
					: 'text-red-600 bg-red-50 dark:text-red-400 dark:bg-red-950'
	);
</script>

<div class="flex flex-col items-center px-3 py-1.5 rounded-xl min-w-14 {colorClass}">
	<span class="text-[0.65rem] font-medium uppercase tracking-wide opacity-85">{label}</span>
	<span class="text-lg font-bold">{score}</span>
</div>
