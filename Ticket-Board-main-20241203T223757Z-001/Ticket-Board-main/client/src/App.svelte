<script>
    import { Router, Route, navigate } from 'svelte-routing';
    import Login from './pages/+Login.svelte';
    import Home from './pages/+Home.svelte';
    import Loading from './pages/+Loading.svelte';

    fetch('/check_credentials')
        .then(response => {
            if (response.ok) {
                navigate('/');
            } else {
                navigate('/login');
            }
        });
</script>

<Router>
    <Route path="/loading" component={Loading} />
    <Route path="/login" component={Login} />
    <Route path="/" component={Home} />
</Router>