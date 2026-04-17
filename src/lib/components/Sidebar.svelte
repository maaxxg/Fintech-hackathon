<script lang="ts">
	import ManagerProfile from './ManagerProfile.svelte';
	import FilterPanel from './FilterPanel.svelte';
</script>

<aside class="flex h-full w-80 shrink-0 flex-col gap-6 overflow-y-auto max-md:w-full" id="sidebar">
	<ManagerProfile />
	<FilterPanel />

	<a
		href="/recommendations"
		class="mt-auto w-full rounded-none border border-blue-700 bg-blue-600 py-3 text-center text-[11px] font-bold tracking-widest text-white uppercase no-underline transition-colors hover:bg-blue-700"
	>
		Contract Recommendations
	</a>
</aside>
