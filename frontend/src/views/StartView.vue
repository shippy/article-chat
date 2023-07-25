<template>
    <div class="content">
        <h1>Welcome to JournalArticle.chat!</h1>
        <p>On your left, you see a sidebar where you'll manage the documents and their associated chats.</p>
        <p>JournalArticle.chat currently only knows how to handle PDFs with OCR'd text within.</p>
    </div>
</template>

<style>
.content {
    grid-area: content;  /* FIXME: Why isn't this enough and I still need to set a left margin? */
    padding: 20px;
    height: 100%;
    margin-left: 320px; /* considering 300px width of sidebar and 20px of some padding */
    overflow-y: auto;
}
</style>