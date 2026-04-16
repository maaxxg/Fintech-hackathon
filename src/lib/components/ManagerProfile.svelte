<script lang="ts">
	import { manager } from '$lib/stores/authStore';
	import { logout } from '$lib/firebase/auth';
	import { goto } from '$app/navigation';

	async function handleLogout(): Promise<void> {
		await logout();
		goto('/login');
	}
</script>

<div
	class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-5"
	id="manager-profile"
>
	{#if $manager}
		<div class="flex items-center gap-3 mb-4">
			<div
				class="w-12 h-12 rounded-full bg-gradient-to-br from-indigo-500 to-indigo-700 text-white flex items-center justify-center font-bold text-xl shrink-0"
			>
				{$manager.name?.charAt(0).toUpperCase() ?? '?'}
			</div>
			<div class="flex flex-col">
				<span class="font-bold text-gray-900 dark:text-gray-100">{$manager.name}</span>
				<span class="text-xs text-gray-500 dark:text-gray-400">{$manager.role}</span>
				<span class="text-xs text-gray-400 dark:text-gray-500">{$manager.branch}</span>
			</div>
		</div>
		<button
			onclick={handleLogout}
			class="w-full py-2 bg-transparent border border-gray-200 dark:border-gray-700 rounded-lg text-gray-500 text-sm cursor-pointer transition-all hover:border-red-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950"
		>
			Sign Out
		</button>
	{:else}
		<p class="text-gray-400 text-center">Loading profile...</p>
	{/if}
</div>
