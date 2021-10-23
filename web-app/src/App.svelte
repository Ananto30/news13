<script>
  import { inview } from "svelte-inview/dist/index";

  import News from "./News.svelte";
  let page = 1;
  let category = "all";
  let fetching = false;
  $: newsList = [];
  const fetchNews = () => {
    fetching = true;
    fetch("https://news13.vercel.app/api/" + category + "?page=" + page)
      .then((data) => data.json())
      .then((data) => {
        console.log(data)
        newsList = [...newsList, ...data];
        fetching = false;
        page++;
      });
  };
  const fetchCategory = (catg) => {
    if (catg != category) {
      newsList = [];
      category = catg;
      page = 1;
      fetchNews();
    }
  };
  fetchNews();
</script>

<main class="container">
  <h1>সর্বশেষ খবর​</h1>
  <h6>
    <!-- svelte-ignore a11y-missing-attribute -->
    <a class="pointer" on:click={() => fetchCategory("all")}>সব</a>
    |
    <!-- svelte-ignore a11y-missing-attribute -->
    <a class="pointer" on:click={() => fetchCategory("bangladesh")}>বাংলাদেশ</a>
    (সূত্র: প্রথম আলো)
  </h6>
  <hr />
  {#if newsList.length > 0}
    <News bind:newsList />
    <div class="center" use:inview={{}} on:change={fetchNews}>
      <button on:click={fetchNews} disabled={fetching}>আরও খবর​</button>
    </div>
  {:else}
    <p class="center">অপেক্ষা করুন​...</p>
  {/if}
</main>

<style>
  .center {
    text-align: center;
  }
  .pointer {
    cursor: pointer;
  }
</style>
