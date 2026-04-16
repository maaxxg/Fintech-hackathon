<script lang="ts">
	import ClientCard from './ClientCard.svelte';
	import { filteredClients, clientsLoading } from '$lib/stores/clientStore';
</script>

<div class="flex-1 flex flex-col min-h-0 bg-white border border-blue-100 rounded-none p-4" id="client-list">
	<div class="flex justify-between items-center mb-4 pb-2 border-b border-blue-100">
		<h2 class="text-[10px] font-bold text-blue-950 uppercase tracking-widest">
			Client Portfolio
		</h2>
		<span class="text-[9px] font-bold uppercase tracking-widest text-blue-600 bg-blue-50 px-1.5 py-0.5 rounded-none border border-blue-200">
			{$filteredClients.length} Clients
		</span>
	</div>

	<!-- Column Headers -->
	<div class="grid grid-cols-[1fr_auto_auto] gap-4 px-3 py-1.5 text-[9px] font-bold uppercase tracking-widest text-blue-500 mb-1 border-b border-blue-50">
		<div>Entity Name</div>
		<div class="w-12 text-center">Risk</div>
		<div class="w-12 text-center">Value</div>
	</div>

	{#if $clientsLoading}
		<div class="flex-1 flex flex-col items-center justify-center text-blue-400 py-10 uppercase tracking-widest text-[10px] font-bold">
			Loading...
		</div>
	{:else if $filteredClients.length === 0}
		<div class="flex-1 flex flex-col items-center justify-center text-blue-400 py-10 text-[10px] uppercase tracking-widest font-bold">
			No records found.
		</div>
	{:else}
		<div class="flex-1 overflow-y-auto flex flex-col pr-1 scrollbar-thin">
			{#each $filteredClients as client (client.id)}
				<ClientCard {client} />
			{/each}
		</div>
	{/if}
</div>
