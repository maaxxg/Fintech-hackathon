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
	class="bg-white border border-blue-100 rounded-none p-4"
	id="manager-profile"
>
	{#if $manager}
		<div class="flex items-center gap-3 mb-4">
			<div
				class="relative w-10 h-10 rounded-none bg-blue-900 border border-blue-950 text-white flex items-center justify-center font-bold text-sm shrink-0"
			>
				{$manager.name?.charAt(0).toUpperCase() ?? '?'}
				<div class="absolute -bottom-1 -right-1 w-2.5 h-2.5 bg-blue-400 border-2 border-white rounded-none z-10"></div>
			</div>
			<div class="flex flex-col">
				<span class="font-bold text-blue-950 text-sm tracking-wide uppercase">{$manager.name}</span>
				<span class="text-[10px] text-blue-600 font-bold tracking-widest uppercase mt-0.5">{$manager.role}</span>
			</div>
		</div>
		<button
			onclick={handleLogout}
			class="w-full py-1.5 bg-white border border-blue-200 rounded-none text-blue-700 text-xs font-bold uppercase tracking-widest transition-colors hover:bg-blue-50 hover:border-blue-300"
		>
			Sign Out
		</button>
	{:else}
		<div class="flex justify-center items-center py-4 text-blue-500 text-[10px] uppercase tracking-widest font-bold">
			Loading
		</div>
	{/if}
</div>
