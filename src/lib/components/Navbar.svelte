<script lang="ts">
</script>

<nav class="sticky top-0 z-50 flex h-10 items-center border-b border-gray-600 bg-gray-700" id="navbar">
	<div class="mx-auto grid w-full max-w-7xl grid-cols-3 items-center px-4">
		<div class="flex justify-start">
			<a
				href="/"
				class="group flex items-center no-underline transition-opacity hover:opacity-80"
			>
				<img src="/logo-snip.png" alt="HPB Logo" class="h-6 w-auto" />
			</a>
		</div>
		<div class="flex justify-center">
			<div class="text-[10px] font-bold tracking-widest text-gray-300 uppercase">
				Bank Management System
			</div>
		</div>
		<div class="flex justify-end hidden md:flex">
			<a
				href="/recommendations"
				class="group flex items-center text-gray-200 no-underline transition-colors hover:text-white"
			>
				<span class="relative text-xs leading-none font-bold tracking-widest uppercase">
					Contract Recommendations
					<span class="absolute -bottom-1.5 left-1/2 h-[2px] w-0 -translate-x-1/2 bg-white transition-all duration-300 ease-out group-hover:w-full"></span>
				</span>
			</a>
		</div>
	</div>
</nav>
