<script>
  import News from './News.svelte'
  let page = 1
  let category = 'all'
  let fetching = false
  $: newsList = []
  const fetchNews = () => {
    fetching = true
    fetch('http://news.dedsec.life/api/news/' + page)
      .then((data) => data.json())
      .then((data) => {
        newsList = [...newsList, ...data.news]
        fetching = false
        page++
      })
  }
  fetchNews()
</script>

<style>
  .center {
    text-align: center;
  }
</style>

<main class="container">
  <h1>সর্বশেষ খবর​</h1>
  <h6>
    <a href="/">সব</a>
    (সূত্র: প্রথম আলো)
  </h6>
  <hr />
  {#if newsList.length > 0}
    <News bind:newsList />
    <div class="center">
      <button on:click={fetchNews} disabled={fetching}>আরও খবর​</button>
    </div>
  {:else}
    <p class="center">অপেক্ষা করুন​...</p>
  {/if}

</main>
