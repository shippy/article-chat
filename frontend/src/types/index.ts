export interface Document {
    id: number;
    title: string;
    chats: Chat[];
}

export interface Message {
    id: number;
    originator: string;
    content: string;
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
