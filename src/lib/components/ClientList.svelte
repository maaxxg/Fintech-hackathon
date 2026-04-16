<script lang="ts">
	import ClientCard from './ClientCard.svelte';
	import { filteredClients, clientsLoading } from '$lib/stores/clientStore';
</script>

<div class="flex-1 flex flex-col min-h-0" id="client-list">
	<div class="flex justify-between items-center mb-4">
		<h2 class="text-xl font-semibold text-gray-900 dark:text-gray-100">Clients</h2>
		<span class="text-sm text-gray-400 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full">
			{$filteredClients.length} clients
		</span>
	</div>

	{#if $clientsLoading}
		<div class="text-center py-12 text-gray-400">
			<div
				class="w-8 h-8 border-3 border-gray-200 dark:border-gray-700 border-t-indigo-500 rounded-full animate-spin mx-auto mb-4"
			></div>
			<p>Loading clients...</p>
		</div>
	{:else if $filteredClients.length === 0}
		<div class="text-center py-12 text-gray-400">
			<p>No clients match your filters</p>
		</div>
	{:else}
		<div class="flex-1 overflow-y-auto flex flex-col gap-2 pr-1 scrollbar-thin">
			{#each $filteredClients as client (client.id)}
				<ClientCard {client} />
			{/each}
		</div>
	{/if}
</div>
