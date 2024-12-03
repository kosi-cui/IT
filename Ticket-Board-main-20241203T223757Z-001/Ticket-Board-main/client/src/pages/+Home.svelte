<script>
	import { onMount } from 'svelte';
	// Component Imports
	import Sidebar from "../components/Sidebar.svelte";
	import TicketTable from "../components/TicketTable.svelte";

	// Globals
	let tickets = [];
	let loading = true;

	function addTicket() {
		fetchTicket(ticket_num).then(ticket => {
			// Get & Parse Tasks
			let ticket_tasks = ticket.tasks;
			let curr_tasks = [];
			if (ticket_tasks.length > 0) {
				curr_tasks = ticket_tasks.map(task => task);
			} else {
				curr_tasks = ['Execute Reimage Sequence'];
			}

			// Set up ticket object
			let curr_ticket = {
				agent: ticket.agent,
				title: ticket.title,
				created_at: ticket.created_at,
				tasks: curr_tasks
			};
			// Need to update via assignment & not push so svelte recognizes the change
			tickets = [...tickets, curr_ticket];
			console.log(tickets);
		});
	}

	async function reimageTickets() {
		const response = await fetch('/api/reimage_tickets');
		const result = await response.json();
		tickets = result;
		loading = false;
		console.log(tickets);
	}

	// Run on page load
	onMount(() => {
		reimageTickets();
	});
</script>

<style>
    .content {
        position: absolute;
        left: 5.1%;
        width: 94.9%;
        height: 100vh;
    }
</style>

<Sidebar topImage="" bottomImage="" />
<div class="content">
	{#if loading}
		<h1>Loading...</h1>
	{:else}
		<TicketTable {tickets} />
	{/if}
</div>