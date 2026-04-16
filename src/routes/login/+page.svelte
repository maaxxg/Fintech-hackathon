<script lang="ts">
	import { login } from '$lib/firebase/auth';
	import { user } from '$lib/stores/authStore';
	import { goto } from '$app/navigation';

	let email = $state('');
	let password = $state('');
	let error = $state('');
	let loading = $state(false);

	$effect(() => {
		if ($user) goto('/');
	});

	async function handleLogin(): Promise<void> {
		error = '';
		loading = true;
		try {
			await login(email, password);
			goto('/');
		} catch (err) {
			error = 'Invalid email or password';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Sign In — ClientGuard</title>
	<meta name="description" content="Sign in to your bank manager dashboard" />
</svelte:head>

<div
	class="min-h-screen flex items-center justify-center bg-white transition-colors"
>
	<div
		class="bg-white border border-blue-200 rounded-none p-10 w-full max-w-sm shadow-none"
	>
		<div class="flex items-center gap-2 mb-8 border-b border-blue-100 pb-4">
			<h1 class="font-bold text-2xl text-blue-950 uppercase tracking-widest m-0">ClientGuard</h1>
		</div>
		
		<h2 class="text-xs font-bold text-blue-500 uppercase tracking-widest mb-1">Access Gateway</h2>
		<p class="text-[10px] text-blue-900/70 mb-6 font-bold uppercase tracking-widest">Authentication Required</p>

		{#if error}
			<div
				class="bg-blue-50 border border-blue-200 text-blue-700 px-3 py-2 rounded-none mb-4 text-[10px] font-bold uppercase tracking-widest"
			>
				{error}
			</div>
		{/if}

		<form onsubmit={(e) => { e.preventDefault(); handleLogin(); }} class="space-y-4">
			<div>
				<label
					for="email"
					class="block text-[10px] font-bold text-blue-900/70 uppercase tracking-widest mb-1.5">Entity Email</label
				>
				<input
					id="email"
					type="email"
					bind:value={email}
					placeholder="sys.admin@bank.corp"
					required
					class="w-full px-3 py-2 bg-white border border-blue-200 rounded-none text-blue-950 text-xs placeholder-blue-300 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
				/>
			</div>

			<div>
				<label
					for="password"
					class="block text-[10px] font-bold text-blue-900/70 uppercase tracking-widest mb-1.5">Authorization Key</label
				>
				<input
					id="password"
					type="password"
					bind:value={password}
					placeholder="••••••••"
					required
					class="w-full px-3 py-2 bg-white border border-blue-200 rounded-none text-blue-950 text-xs placeholder-blue-300 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
				/>
			</div>

			<button
				type="submit"
				disabled={loading}
				class="w-full mt-2 py-2 bg-blue-600 hover:bg-blue-700 text-white text-[10px] font-bold uppercase tracking-widest rounded-none border border-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
			>
				{loading ? 'Authenticating...' : 'Initialize Session'}
			</button>
		</form>
	</div>
</div>
