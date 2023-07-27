<template>
  <div class="landing-page">
    <section class="hero">
      <h1>Chat with Journal Articles</h1>
      <p>Upload your documents and discuss them in a unique chat interface!</p>
      <p><a href="https://www.linkedin.com/in/simonpodhajsky">Contact Simon for beta access.</a></p>
    </section>
    <section class="features">
      <div class="feature">
        <div class="illustration"><img src="/feature_upload.png" /></div>
        <h2>Upload Your Documents</h2>
        <p>Upload your documents and convert them into vector embeddings.</p>
      </div>
      <div class="feature">
        <div class="illustration"><img src="/feature_chat.png" /></div>
        <h2>Start a Chat</h2>
        <p>Start a chat and discuss your documents in a structured way.</p>
      </div>
      <div class="feature">
        <div class="illustration"><img src="/feature_search.png" /></div>
        <h2>Advanced Search <em>(coming soon...)</em></h2>
        <p>Use our advanced search to find specific documents parts by their meaning.</p>
      </div>
    </section>
  </div>
</template>

<style scoped>
.landing-page {
  text-align: center;
}

.hero {
  padding: 50px;
}

.features {
  display: flex;
  justify-content: space-around;
  padding: 50px;
}

.feature {
  width: 30%;
}

.illustration img {
  width: 100%;
}
</style>
