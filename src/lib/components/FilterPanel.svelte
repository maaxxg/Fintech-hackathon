<script lang="ts">
	import { filters } from '$lib/stores/clientStore';
	import type { FilterState, } from '$lib/types';
	import type { PriorityAction } from '$lib/priority';

	const ACTION_OPTIONS: { value: PriorityAction; label: string; cls: string; active: string }[] = [
		{ value: 'high_priority_retention', label: 'Retain',  cls: 'border-red-300 text-red-700 bg-white',         active: 'bg-red-600 text-white border-red-700' },
		{ value: 'monitor_high_value',      label: 'Monitor', cls: 'border-amber-300 text-amber-700 bg-white',      active: 'bg-amber-500 text-white border-amber-600' },
		{ value: 'nurture',                 label: 'Nurture', cls: 'border-green-300 text-green-700 bg-white',      active: 'bg-green-600 text-white border-green-700' },
		{ value: 'no_action',               label: 'Low Priority', cls: 'border-gray-300 text-gray-500 bg-white',   active: 'bg-gray-500 text-white border-gray-600' },
	];

	function toggleAction(value: PriorityAction) {
		filters.update((f) => {
			const already = f.actions.includes(value);
			return { ...f, actions: already ? f.actions.filter((a) => a !== value) : [...f.actions, value] };
		});
	}

	function updateFilter<K extends keyof FilterState>(key: K, value: FilterState[K]): void {
		filters.update((f) => ({ ...f, [key]: value }));
	}

	function resetFilters(): void {
		filters.set({
			search: '',
			riskMin: 0,
			riskMax: 100,
			valueMin: 0,
			valueMax: 100,
			actions: [],
			sortBy: null,
			sortDir: 'desc'
		});
	}
</script>

<div class="rounded-none border border-red-100 bg-white p-4" id="filter-panel">
	<div class="mb-4 flex items-center justify-between border-b border-red-100 pb-2">
		<h3 class="m-0 text-[10px] font-bold tracking-widest text-red-950 uppercase">Filters</h3>
		<button
			onclick={resetFilters}
			class="text-[10px] font-bold tracking-widest text-red-500 uppercase hover:text-red-800"
		>
			Clear
		</button>
	</div>

	<!-- Action filter -->
	<div class="mb-4">
		<span class="mb-2 block text-[10px] font-bold tracking-widest text-red-900/70 uppercase">Priority Action</span>
		<div class="flex flex-wrap gap-1.5">
			{#each ACTION_OPTIONS as opt}
				<button
					onclick={() => toggleAction(opt.value)}
					class="rounded-none border px-2 py-0.5 text-[10px] font-bold tracking-widest uppercase transition-colors {$filters.actions.includes(opt.value) ? opt.active : opt.cls}"
				>
					{opt.label}
				</button>
			{/each}
		</div>
	</div>

	<!-- Search -->
	<div class="mb-4">
		<label for="search-filter" class="mb-1.5 block text-[10px] font-bold tracking-widest text-red-900/70 uppercase">Search</label>
		<input
			id="search-filter"
			type="text"
			placeholder="Enter name..."
			value={$filters.search}
			oninput={(e) => updateFilter('search', (e.target as HTMLInputElement).value)}
			class="w-full rounded-none border border-red-200 bg-white px-2.5 py-1.5 text-xs text-red-950 focus:border-red-500 focus:ring-1 focus:ring-red-500 focus:outline-none"
		/>
	</div>

	<!-- Risk Score Range -->
	<div class="mb-4">
		<span class="mb-1.5 block text-[10px] font-bold tracking-widest text-red-900/70 uppercase">Risk Profile</span>
		<div class="flex items-center gap-1.5">
			<input
				type="number" min="0" max="100"
				value={$filters.riskMin}
				oninput={(e) => updateFilter('riskMin', +(e.target as HTMLInputElement).value)}
				class="flex-1 rounded-none border border-red-200 bg-white px-2 py-1.5 text-center text-xs text-red-950 focus:border-red-500 focus:ring-1 focus:ring-red-500 focus:outline-none"
			/>
			<span class="text-xs text-red-200">-</span>
			<input
				type="number" min="0" max="100"
				value={$filters.riskMax}
				oninput={(e) => updateFilter('riskMax', +(e.target as HTMLInputElement).value)}
				class="flex-1 rounded-none border border-red-200 bg-white px-2 py-1.5 text-center text-xs text-red-950 focus:border-red-500 focus:ring-1 focus:ring-red-500 focus:outline-none"
			/>
		</div>
	</div>

	<!-- Value Score Range -->
	<div class="mb-1">
		<span class="mb-1.5 block text-[10px] font-bold tracking-widest text-red-900/70 uppercase">Value</span>
		<div class="flex items-center gap-1.5">
			<input
				type="number" min="0" max="100"
				value={$filters.valueMin}
				oninput={(e) => updateFilter('valueMin', +(e.target as HTMLInputElement).value)}
				class="flex-1 rounded-none border border-red-200 bg-white px-2 py-1.5 text-center text-xs text-red-950 focus:border-red-500 focus:ring-1 focus:ring-red-500 focus:outline-none"
			/>
			<span class="text-xs text-red-200">-</span>
			<input
				type="number" min="0" max="100"
				value={$filters.valueMax}
				oninput={(e) => updateFilter('valueMax', +(e.target as HTMLInputElement).value)}
				class="flex-1 rounded-none border border-red-200 bg-white px-2 py-1.5 text-center text-xs text-red-950 focus:border-red-500 focus:ring-1 focus:ring-red-500 focus:outline-none"
			/>
		</div>
	</div>
</div>
