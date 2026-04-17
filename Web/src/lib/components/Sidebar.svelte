<script lang="ts">
	import ManagerProfile from './ManagerProfile.svelte';
	import FilterPanel from './FilterPanel.svelte';
</script>

<aside class="flex h-full w-80 shrink-0 flex-col gap-6 overflow-hidden max-md:w-full" id="sidebar">
	<ManagerProfile />
	<FilterPanel />

	<div class="mt-auto mb-4 flex grow items-center justify-center min-h-0">
		<img src="/Hpb-logo.svg.png" alt="HPB Logo" class="h-full w-auto max-w-[16rem] object-contain mix-blend-multiply" />
	</div>
</aside>
