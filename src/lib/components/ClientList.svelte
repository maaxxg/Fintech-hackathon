<script lang="ts">
	import ClientCard from './ClientCard.svelte';
	import { filteredClients, clientsLoading } from '$lib/stores/clientStore';
</script>

<div
	class="flex min-h-0 flex-1 flex-col rounded-none border border-blue-100 bg-white p-4"
	id="client-list"
>
	<div class="mb-4 flex items-center justify-between border-b border-blue-100 pb-2">
		<h2 class="text-[11px] font-bold tracking-widest text-blue-950 uppercase">Client Portfolio</h2>
		<span
			class="rounded-none border border-blue-200 bg-blue-50 px-1.5 py-0.5 text-[10px] font-bold tracking-widest text-blue-600 uppercase"
		>
			{$filteredClients.length} Clients
		</span>
	</div>

	<!-- Column Headers -->
	<div
		class="mb-1 grid grid-cols-[1fr_auto_auto] gap-4 border-b border-blue-50 px-3 py-1.5 pl-4 text-[10px] font-bold tracking-widest text-blue-500 uppercase"
	>
		<div>Entity Name</div>
		<div class="w-12 text-center">Risk</div>
		<div class="w-12 text-center">Value</div>
	</div>

	{#if $clientsLoading}
		<div
			class="flex flex-1 flex-col items-center justify-center py-10 text-[11px] font-bold tracking-widest text-blue-400 uppercase"
		>
			Loading...
		</div>
	{:else if $filteredClients.length === 0}
		<div
			class="flex flex-1 flex-col items-center justify-center py-10 text-[11px] font-bold tracking-widest text-blue-400 uppercase"
		>
			No records found.
		</div>
	{:else}
		<div class="scrollbar-thin flex flex-1 flex-col overflow-y-auto pr-1">
			{#each $filteredClients as client (client.id)}
				<ClientCard {client} />
			{/each}
		</div>
	{/if}
</div>
