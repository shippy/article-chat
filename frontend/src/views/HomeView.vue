<template>
  <div class="landing-page">
    <section class="hero">
      <h1>Chat with Journal Articles</h1>
      <p>Upload your documents and chat with their contents!</p>
      <p><a href="https://www.linkedin.com/in/simonpodhajsky">Contact Simon for beta access.</a></p>
    </section>
    <section class="features">
      <div class="feature">
        <div class="illustration"><img src="/feature_upload.png" /></div>
        <h2>Upload Your Documents</h2>
        <p>Upload and convert your PDFs into vector embeddings.</p>
      </div>
      <div class="feature">
        <div class="illustration"><img src="/feature_chat.png" /></div>
        <h2>Start a Chat</h2>
        <p>Chat up your documents in a structured way.</p>
      </div>
      <div class="feature">
        <div class="illustration"><img src="/feature_search.png" /></div>
        <h2>Advanced Search <em>(coming soon!)</em></h2>
        <p>Find specific document parts by their text or meaning.</p>
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
  flex-wrap: wrap;
}

.feature {
  width: 30%;
  margin-bottom: 30px;
}

/* Responsive Design */
@media only screen and (max-width: 800px) {
  .features {
    flex-direction: column;
    align-items: center;
  }
  
  .feature {
    width: 80%;
  }
}

.illustration img {
  width: 100%;
}
</style>
