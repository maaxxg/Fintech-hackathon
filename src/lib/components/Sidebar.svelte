<script lang="ts">
	import ManagerProfile from './ManagerProfile.svelte';
	import FilterPanel from './FilterPanel.svelte';
</script>

<aside class="w-80 shrink-0 flex flex-col gap-6 h-full overflow-y-auto max-md:w-full" id="sidebar">
	<ManagerProfile />
	<FilterPanel />
	
	<a 
		href="/recommendations"
		class="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white text-[11px] font-bold uppercase tracking-widest rounded-none border border-blue-700 transition-colors text-center no-underline mt-auto"
	>
		Contract Recommendations
	</a>
</aside>
