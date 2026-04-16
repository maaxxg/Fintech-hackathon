<script lang="ts">
	import ThemeToggle from './ThemeToggle.svelte';
</script>

<nav
	class="h-16 bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl border-b border-gray-200 dark:border-gray-800 sticky top-0 z-50"
	id="navbar"
>
	<div class="max-w-7xl mx-auto h-full flex items-center justify-between px-6">
		<a href="/" class="flex items-center gap-2 no-underline">
			<span class="text-2xl">🏦</span>
			<span class="font-bold text-xl text-gray-900 dark:text-gray-100">ClientGuard</span>
		</a>
		<ThemeToggle />
	</div>
</nav>
