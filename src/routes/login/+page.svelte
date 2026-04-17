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

<div class="flex min-h-screen bg-white transition-colors">
	<!-- Left panel: Branding -->
	<div
		class="hidden flex-1 flex-col items-center justify-center border-r border-blue-900 bg-blue-950 px-12 md:flex"
	>
		<h1 class="m-0 mb-4 text-4xl font-extrabold tracking-widest text-white uppercase">
			ClientGuard
		</h1>
		<p
			class="m-0 max-w-xs text-center text-[11px] leading-relaxed font-bold tracking-widest text-blue-300 uppercase"
		>
			Bank Client Retention Management System
		</p>
		<div class="mt-8 h-px w-16 bg-blue-800"></div>
	</div>

	<!-- Right panel: Login form -->
	<div class="flex flex-1 items-center justify-center bg-white p-8">
		<div class="w-full max-w-sm">
			<div class="mb-8 flex items-center gap-2 border-b border-blue-100 pb-4 md:hidden">
				<h1 class="m-0 text-2xl font-bold tracking-widest text-blue-950 uppercase">ClientGuard</h1>
			</div>

			<h2 class="mb-1 text-xs font-bold tracking-widest text-blue-500 uppercase">Access Gateway</h2>
			<p class="mb-6 text-[11px] font-bold tracking-widest text-blue-900/70 uppercase">
				Authentication Required
			</p>

			{#if error}
				<div
					class="mb-4 rounded-none border border-blue-200 bg-blue-50 px-3 py-2 text-[11px] font-bold tracking-widest text-blue-700 uppercase"
				>
					{error}
				</div>
			{/if}

			<form
				onsubmit={(e) => {
					e.preventDefault();
					handleLogin();
				}}
				class="space-y-4"
			>
				<div>
					<label
						for="email"
						class="mb-1.5 block text-[11px] font-bold tracking-widest text-blue-900/70 uppercase"
						>Entity Email</label
					>
					<input
						id="email"
						type="email"
						bind:value={email}
						placeholder="sys.admin@bank.corp"
						required
						class="w-full rounded-none border border-blue-200 bg-white px-3 py-2 text-sm text-blue-950 placeholder-blue-300 transition focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
					/>
				</div>

				<div>
					<label
						for="password"
						class="mb-1.5 block text-[11px] font-bold tracking-widest text-blue-900/70 uppercase"
						>Authorization Key</label
					>
					<input
						id="password"
						type="password"
						bind:value={password}
						placeholder="••••••••"
						required
						class="w-full rounded-none border border-blue-200 bg-white px-3 py-2 text-sm text-blue-950 placeholder-blue-300 transition focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
					/>
				</div>

				<button
					type="submit"
					disabled={loading}
					class="mt-2 w-full rounded-none border border-blue-700 bg-blue-600 py-2.5 text-[11px] font-bold tracking-widest text-white uppercase transition-colors hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
				>
					{loading ? 'Authenticating...' : 'Initialize Session'}
				</button>
			</form>
		</div>
	</div>
</div>
