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

<div
	class="inline-flex items-center justify-center rounded-none px-1.5 py-0.5 font-mono text-[10px] {colorClass} gap-1 border"
>
	{#if label}
		<span class="font-sans font-bold tracking-widest uppercase opacity-80">{label}:</span>
	{/if}
	<span class="flex items-center gap-0.5 font-bold">
		{score}
		{#if arrow}
			<span class="text-[10px]">{arrow}</span>
		{/if}
	</span>
</div>
