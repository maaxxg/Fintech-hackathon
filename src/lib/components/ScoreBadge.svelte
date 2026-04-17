<script lang="ts">
	let { label = '', score = 0, type = 'risk' } = $props();

	// Just shades of blue based on intensity to keep it monochrome
	let colorClass = $derived(
		score >= 70
			? 'text-blue-900 bg-blue-100 border-blue-900'
			: score >= 40
				? 'text-blue-700 bg-white border-blue-300'
				: 'text-blue-500 bg-white border-blue-200'
	);
	
	let arrow = $derived(score >= 70 ? '↑' : score >= 40 ? '' : '↓');
</script>

<div class="inline-flex items-center justify-center px-1.5 py-0.5 rounded-none font-mono text-xs {colorClass} border gap-1">
	{#if label}
		<span class="opacity-80 font-sans tracking-widest uppercase font-bold text-[10px]">{label}:</span>
	{/if}
	<span class="font-bold flex items-center gap-0.5 text-base">
		{score}
		{#if arrow}
			<span class="text-[10px]">{arrow}</span>
		{/if}
	</span>
</div>
