<script>
  import { fade } from "svelte/transition";
  import moment from "moment";
  import 'moment/locale/bn-bd';

  export let newsList;
  // moment.locale("bn-bd");

  let sharingSupported = navigator.share ? true : false;

  const share = (news) => {
    navigator
      .share({
        title: news.title,
        url: news.link,
      })
      .then(() => {
        console.log("Thanks for sharing!");
      })
      .catch(console.error);
  };
</script>

{#each newsList as news}
  {#if news.published_time != ""}
    <div in:fade>
      <h4>{news.title}</h4>
      <h6>
        {moment(news.published_time).fromNow()} | {news.category} | {news.author}
        <span>
          {#if sharingSupported}
            <button class="shareBtn" on:click={() => share(news)}>
              [ শেয়ার ]
            </button>
          {/if}
        </span>
      </h6>
      <p>
        {news.summary}
        <a href={news.link} target="_blank">বিস্তারিত</a>
      </p>
      <hr />
    </div>
  {/if}
{/each}

<style>
  .shareBtn {
    border: 0ch;
    margin: 0;
    padding: 0;
    font-size: 12px;
    text-decoration: underline;
    color: #6fc0aa;
  }
</style>
