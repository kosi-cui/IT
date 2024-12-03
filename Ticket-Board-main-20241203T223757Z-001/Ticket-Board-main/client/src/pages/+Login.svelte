<script>
    import { navigate } from 'svelte-routing';
    let api_key = '';
    let url = '';

    async function submitForm() {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ api_key, url })
    });

    if (response.ok) {
        navigate('/')
    } else {
      console.log('Failed to save credentials.');
    }
  }
</script>

<h2>Login</h2>
<form on:submit|preventDefault={submitForm}>
  <label for="api_key">API Key:</label><br>
  <input type="text" bind:value={api_key} id="api_key" name="api_key"><br>
  <label for="url">URL:</label><br>
  <input type="text" bind:value={url} id="url" name="url"><br>
  <input type="submit" value="Submit">
</form>