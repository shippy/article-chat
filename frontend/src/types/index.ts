export interface Document {
    id: number;
    name: string;
    chats: Chat[];
}

export interface Message {
    id: number;
    text: string;
}

export interface Chat {
    id: number;
    state: ChatState;
}

export interface ChatState {
    messages: Message[];
}

export interface DocumentsState {
    documents: Document[];
}
