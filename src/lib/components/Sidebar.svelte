<script lang="ts">
	import ManagerProfile from './ManagerProfile.svelte';
	import FilterPanel from './FilterPanel.svelte';
</script>

<aside class="flex h-full w-80 shrink-0 flex-col gap-6 overflow-y-auto max-md:w-full" id="sidebar">
	<ManagerProfile />
	<FilterPanel />

	<div class="mt-auto mb-4 flex items-center justify-center">
		<img src="/logo.png" alt="CCG Logo" class="h-auto w-64 object-contain mix-blend-multiply" />
	</div>
</aside>
