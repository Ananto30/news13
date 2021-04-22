<script>
  import { prevent_default } from 'svelte/internal'

  import News from './News.svelte'
  let page = 1
  let category = 'all'
  let fetching = false
  $: newsList = []
  const fetchNews = () => {
    fetching = true
    fetch('https://liqlerzyj8.execute-api.ap-southeast-1.amazonaws.com/news13/api/news/' + category + '/' + page)
      .then((data) => data.json())
      .then((data) => {
        newsList = [...newsList, ...data.news]
        fetching = false
        page++
      })
  }
  const fetchCategory = (catg) => {
    if (catg != category) {
      newsList = []
      category = catg
      page = 1
      fetchNews()
    }
  }
  fetchNews()
</script>

<style>
  .center {
    text-align: center;
  }
  .pointer {
    cursor: pointer;
  }
</style>

<main class="container">
  <h1>সর্বশেষ খবর​</h1>
  <h6>
    <a class="pointer" on:click={() => fetchCategory('all')}>সব</a>
    |
    <a class="pointer" on:click={() => fetchCategory('bangladesh')}>বাংলাদেশ</a>
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
