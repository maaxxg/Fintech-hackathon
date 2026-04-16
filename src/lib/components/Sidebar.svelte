<script lang="ts">
	import ManagerProfile from './ManagerProfile.svelte';
	import FilterPanel from './FilterPanel.svelte';
</script>

<aside class="w-80 shrink-0 flex flex-col gap-4 h-full overflow-y-auto max-md:w-full" id="sidebar">
	<ManagerProfile />
	<FilterPanel />
</aside>
