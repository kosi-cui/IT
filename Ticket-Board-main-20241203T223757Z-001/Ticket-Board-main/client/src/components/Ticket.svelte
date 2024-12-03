<script>
    export let agent_name = "";
    export let title = "";
    export let date = "";
    export let tasks = [];
</script>

<style>
    td {
        border: 1px solid black;
        padding: 8px;
        text-align: left;
    }
</style>
<!--
<div>
    <h2>{title}</h2>
    <p>Agent: {agent_name}</p>
    <p>Date: {date}</p>
    <p>Tasks: <select>
        {#each tasks as task, index (task)}
            <option selected={index === 0}>{task}</option>
        {/each}
    </select></p>
</div>
-->

<tr>
    <!-- <td>{ticket.number}</td> -->
    <td>{title}</td>
    <td>{agent_name}</td>
    <td>{date}</td>
    <td>
        <select>
            {#each tasks as task, index (task)}
                <option selected={index === 0}>{task}</option>
            {/each}
        </select>
    </td>
</tr>