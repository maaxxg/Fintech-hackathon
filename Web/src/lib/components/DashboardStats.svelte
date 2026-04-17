<script lang="ts">
	import { filteredClients } from '$lib/stores/clientStore';

	let totalClients = $derived($filteredClients.length);
	let avgRisk = $derived(
		totalClients > 0
			? Math.round($filteredClients.reduce((sum, c) => sum + c.riskScore, 0) / totalClients)
			: 0
	);
	let avgValue = $derived(
		totalClients > 0
			? Math.round($filteredClients.reduce((sum, c) => sum + c.valueScore, 0) / totalClients)
			: 0
	);
	let highRisk = $derived($filteredClients.filter((c) => c.riskScore >= 70).length);
</script>

<div class="mb-4 grid grid-cols-2 gap-4 md:grid-cols-4" id="dashboard-stats">
	<div class="rounded-none border border-red-100 bg-white p-4">
		<span class="mb-1 block text-[11px] font-bold tracking-widest text-red-500 uppercase"
			>Total Clients</span
		>
		<span class="text-2xl font-extrabold text-red-950">{totalClients}</span>
	</div>
	<div class="rounded-none border border-red-100 bg-white p-4">
		<span class="mb-1 block text-[11px] font-bold tracking-widest text-red-500 uppercase"
			>Avg Risk</span
		>
		<span class="text-2xl font-extrabold text-red-950">{avgRisk}</span>
	</div>
	<div class="rounded-none border border-red-100 bg-white p-4">
		<span class="mb-1 block text-[11px] font-bold tracking-widest text-red-500 uppercase"
			>Avg Value</span
		>
		<span class="text-2xl font-extrabold text-red-950">{avgValue}</span>
	</div>
	<div class="rounded-none border border-red-100 bg-white p-4">
		<span class="mb-1 block text-[11px] font-bold tracking-widest text-red-500 uppercase"
			>High Risk</span
		>
		<span class="text-2xl font-extrabold text-red-950">{highRisk}</span>
	</div>
</div>
