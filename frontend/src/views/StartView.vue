<script setup lang="ts">
import Sidebar from '@/components/Sidebar.vue';
</script>

<template>
    <Sidebar />
    <div className="content">
        <div id="start">
            <h1>Welcome to JournalArticle.chat!</h1>
            <p>On your left, you see a sidebar where you'll manage the documents and their associated chats.</p>
            <p>We're currently working within the following constraints:</p>
            <ol>
                <li>JournalArticle.chat currently only knows how to handle PDFs with OCR'd text within.</li>
                <li>While nominally a chat, JournalArticle.chat only recalls the previous two messages.</li>
            </ol>
            <p>Here's how this whole thing works:</p>
            <ol>
                <li>The PDF file you've uploaded is split into chunks of ~1000 characters.</li>
                <li>
                    The chunks are converted into vector embeddings using OpenAI. This basically converts
                    the meaning of the text into a vector of numbers. This means each chunk can be compared
                    against any other embedding to see how similar they are.
                </li>
                <li>You create a chat and ask a question.</li>
                <li>Your question is converted into the same vector embedding as your document chunks.</li>
                <li>
                    We search the database for document chunks that are semantically most like your question,
                    meaning that its vector representation is the least distant from the chunk's vector representation.
                </li>
                <li>
                    We retrieve the chunks, integrate them into an instruction template, and send it
                    (along with the previous question &amp; answer if available) to GPT-4 to make sense of.
                </li>
                <li>We get the response from GPT-4 and show it to you.</li>
            </ol>
            <p><strong>This means that there are a couple of limitations to the capacities of this tool:</strong></p>
            <ul>
                <li>
                    Questions that don't look semantically like their answers are a crapshoot.
                    (For example, "who are the authors of this paper" is unlikely to retrieve 
                    the author list, even though it's been converted into embeddings along with
                    everything else.)
                </li>
                <li>
                    The OpenAI embeddings are trained on a corpus of text that is mostly English.
                    Similarity search within other languages is unlikely to work well.
                </li>
            </ul>
        </div>
    </div>
</template>

<style>
.content {
    grid-area: content;
    /* FIXME: Why isn't this enough and I still need to set a left margin? */
    padding: 20px;
    height: 100%;
    overflow-y: auto;
    margin-bottom: 100px;
}

p,
ol,
ul {
    margin-bottom: 1em;
}

#start {
    margin-left: 320px;
    /* considering 300px width of sidebar and 20px of some padding */
    width: calc(100% - 320px);
    /* considering 300px width of sidebar and 20px of some padding */
}
</style>