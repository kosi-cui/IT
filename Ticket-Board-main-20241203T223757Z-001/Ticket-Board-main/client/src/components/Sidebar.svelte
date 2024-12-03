<script>
    export let topImage = "";
    export let bottomImage = "";
    let color = "[[color:accent]]";
</script>

<style>
    .sidebar {
        position: fixed;
        top: 0;
        left: 0;
        width: 5%;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .sidebar img {
        width: 100%;
        height: auto;
    }
</style>

<div class="sidebar" style="background-color: {color};">
    <img src={topImage} alt="Top">
    <img src={bottomImage} alt="Bottom">
</div>