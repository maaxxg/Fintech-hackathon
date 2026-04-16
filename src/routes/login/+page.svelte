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
	class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950 p-4 transition-colors"
>
	<div
		class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-10 w-full max-w-md shadow-lg"
	>
		<div class="flex items-center gap-2 mb-6">
			<span class="text-3xl">🏦</span>
			<span class="font-bold text-2xl text-gray-900 dark:text-gray-100">ClientGuard</span>
		</div>
		<h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-1">Welcome Back</h1>
		<p class="text-gray-500 dark:text-gray-400 mb-6">Sign in to your manager dashboard</p>

		{#if error}
			<div
				class="bg-red-50 dark:bg-red-950 text-red-600 dark:text-red-400 px-4 py-3 rounded-lg mb-4 text-sm"
			>
				{error}
			</div>
		{/if}

		<form onsubmit={(e) => { e.preventDefault(); handleLogin(); }} class="space-y-5">
			<div>
				<label
					for="email"
					class="block text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">Email</label
				>
				<input
					id="email"
					type="email"
					bind:value={email}
					placeholder="manager@bank.com"
					required
					class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500 transition"
				/>
			</div>

			<div>
				<label
					for="password"
					class="block text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">Password</label
				>
				<input
					id="password"
					type="password"
					bind:value={password}
					placeholder="••••••••"
					required
					class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500 transition"
				/>
			</div>

			<button
				type="submit"
				disabled={loading}
				class="w-full py-3 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition-all hover:-translate-y-0.5 active:translate-y-0"
			>
				{loading ? 'Signing in...' : 'Sign In'}
			</button>
		</form>
	</div>
</div>
