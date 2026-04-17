<script lang="ts">
	let { label = '', score = 0 } = $props();

	// Just shades of blue based on intensity to keep it monochrome
	let colorClass = $derived(
		score >= 70
			? 'text-red-900 bg-red-100 border-red-900'
			: score >= 40
				? 'text-red-700 bg-white border-red-300'
				: 'text-red-500 bg-white border-red-200'
	);

	let arrow = $derived(score >= 70 ? '↑' : score >= 40 ? '' : '↓');
</script>

<div
	class="inline-flex items-center justify-center rounded-none px-1 py-0.5 font-mono text-[11px] {colorClass} gap-1 border"
>
	{#if label}
		<span class="font-sans font-bold tracking-widest uppercase opacity-80 text-[11px]">{label}:</span>
	{/if}
	<span class="flex items-center gap-0.5 font-bold">
		{score}
		{#if arrow}
			<span class="text-[10px] font-black">{arrow}</span>
		{/if}
	</span>
</div>
