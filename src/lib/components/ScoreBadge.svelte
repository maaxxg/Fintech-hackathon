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
</script>

<div class="inline-flex items-center justify-center px-1.5 py-0.5 rounded-none font-mono text-[10px] {colorClass} border">
	{#if label}
		<span class="mr-1 opacity-80 font-sans tracking-widest uppercase font-bold">{label}:</span>
	{/if}
	<span class="font-bold">{score}</span>
</div>
