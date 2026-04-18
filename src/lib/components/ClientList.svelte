<script lang="ts">
	import ClientCard from './ClientCard.svelte';
	import { filteredClients, clientsLoading, filters } from '$lib/stores/clientStore';

	function toggleSort(col: 'risk' | 'value') {
		filters.update((f) => {
			if (f.sortBy === col) {
				return { ...f, sortDir: f.sortDir === 'desc' ? 'asc' : 'desc' };
			}
			return { ...f, sortBy: col, sortDir: 'desc' };
		});
	}

	function sortIcon(col: 'risk' | 'value'): string {
		if ($filters.sortBy !== col) return '↕';
		return $filters.sortDir === 'desc' ? '↓' : '↑';
	}
</script>

<div
	class="flex min-h-0 flex-1 flex-col rounded-none border border-red-100 bg-white p-4"
	id="client-list"
>
	<div class="mb-4 flex items-center justify-between border-b border-red-100 pb-2">
		<h2 class="text-[11px] font-bold tracking-widest text-red-950 uppercase">Client Portfolio</h2>
		<span
			class="rounded-none border border-red-200 bg-red-50 px-1.5 py-0.5 text-[10px] font-bold tracking-widest text-red-600 uppercase"
		>
			{$filteredClients.length} Clients
		</span>
	</div>

	<!-- Column Headers -->
	<div
		class="mb-1 grid grid-cols-[1fr_auto_auto_auto] items-center gap-4 border-b border-red-50 px-3 py-1.5 pl-4 text-[10px] font-bold tracking-widest text-red-500 uppercase"
	>
		<div>Entity Name</div>
		<div class="w-16 text-center">Action</div>
		<button
			onclick={() => toggleSort('risk')}
			class="flex w-12 cursor-pointer items-center justify-center gap-0.5 text-[10px] font-bold tracking-widest uppercase transition-colors hover:text-red-800 {$filters.sortBy === 'risk' ? 'text-red-700' : ''}"
		>
			Risk <span class="font-mono text-[11px]">{sortIcon('risk')}</span>
		</button>
		<button
			onclick={() => toggleSort('value')}
			class="flex w-12 cursor-pointer items-center justify-center gap-0.5 text-[10px] font-bold tracking-widest uppercase transition-colors hover:text-red-800 {$filters.sortBy === 'value' ? 'text-red-700' : ''}"
		>
			Value <span class="font-mono text-[11px]">{sortIcon('value')}</span>
		</button>
	</div>

	{#if $clientsLoading}
		<div
			class="flex flex-1 flex-col items-center justify-center py-10 text-[11px] font-bold tracking-widest text-red-400 uppercase"
		>
			Loading...
		</div>
	{:else if $filteredClients.length === 0}
		<div
			class="flex flex-1 flex-col items-center justify-center py-10 text-[11px] font-bold tracking-widest text-red-400 uppercase"
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
