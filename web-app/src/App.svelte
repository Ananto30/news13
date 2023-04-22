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
        console.log(data);
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
  <div class="fixed">
    <h6 class="inside">
      <!-- svelte-ignore a11y-missing-attribute -->
      <a class="pointer" on:click={() => fetchCategory("all")}>
        <span class={category === "all" ? "underline" : ""}> সব </span>
      </a>
      |
      <!-- svelte-ignore a11y-missing-attribute -->
      <a class="pointer" on:click={() => fetchCategory("bangladesh")}>
        <span class={category === "bangladesh" ? "underline" : ""}>
          বাংলাদেশ
        </span>
      </a>
      <span class="right font-light">(সূত্র: প্রথম আলো)</span>
    </h6>
  </div>

  <div class="top-padding">
    <h1>সর্বশেষ খবর​</h1>
    <hr />
    {#if newsList.length > 0}
      <News bind:newsList />
      <div class="center" use:inview={{}} on:change={fetchNews}>
        <button on:click={fetchNews} disabled={fetching}>আরও খবর​</button>
      </div>
    {:else}
      <p class="center">অপেক্ষা করুন​...</p>
    {/if}
  </div>
</main>

<style>
  .center {
    text-align: center;
  }
  .pointer {
    cursor: pointer;
  }

  .fixed {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: #fff;
    padding: 1rem;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }

  .inside {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 4rem;
  }

  @media (max-width: 50em) {
    .inside {
      padding: 0 0.5rem;
    }
  }

  .top-padding {
    padding-top: 3rem;
  }

  .underline {
    text-decoration: underline;
  }

  .right {
    float: right;
  }

  .font-light {
    font-weight: 300;
  }
</style>
