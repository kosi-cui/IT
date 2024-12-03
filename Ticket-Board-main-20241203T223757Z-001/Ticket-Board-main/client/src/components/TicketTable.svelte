<script>
    import Ticket from './Ticket.svelte';
    export let tickets = []; // Array of ticket objects
</script>

<style>
    table {
        width: 100%;
        border-collapse: collapse;
    }

    th {
        border: 1px solid black;
        padding: 8px;
        text-align: left;
    }

    th {
        background-color: #f2f2f2;
    }
</style>

<table>
    <tr>
        <!-- <th>Ticket Number</th> -->
        <th>Title</th>
        <th>Agent</th>
        <th>Created At</th>
        <th>Tasks</th>
    </tr>
    {#each tickets as ticket}
        <Ticket agent_name={ticket.agent} title={ticket.title} date={ticket.created_at} tasks={ticket.tasks} />
    {/each}
</table>