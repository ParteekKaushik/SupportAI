"use client";

import { FormEvent, useState } from "react";

import { sendMessage } from "@/lib/api";

type Message = {
  role: "user" | "assistant";
  content: string;
};

type Conversation = {
  id: string;
  title: string;
  messages: Message[];
};

function createConversation(): Conversation {
  return {
    id: crypto.randomUUID(),
    title: "New chat",
    messages: [],
  };
}

export default function Home() {
  const [conversations, setConversations] = useState<Conversation[]>([
    createConversation(),
  ]);

  const [activeConversationId, setActiveConversationId] =
    useState<string>(conversations[0].id);

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const activeConversation = conversations.find(
    (conversation) =>
      conversation.id === activeConversationId,
  );

  const messages = activeConversation?.messages ?? [];

  function createNewChat() {
    const newConversation = createConversation();

    setConversations((previous) => [
      ...previous,
      newConversation,
    ]);

    setActiveConversationId(newConversation.id);
    setMessage("");
  }

  function updateConversationMessages(
    conversationId: string,
    newMessages: Message[],
  ) {
    setConversations((previous) =>
      previous.map((conversation) =>
        conversation.id === conversationId
          ? {
              ...conversation,
              messages: newMessages,
            }
          : conversation,
      ),
    );
  }

  function updateConversationTitle(
    conversationId: string,
    title: string,
  ) {
    setConversations((previous) =>
      previous.map((conversation) =>
        conversation.id === conversationId
          ? {
              ...conversation,
              title,
            }
          : conversation,
      ),
    );
  }

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    const trimmedMessage = message.trim();

    if (!trimmedMessage || loading || !activeConversation) {
      return;
    }

    const conversationId = activeConversation.id;

    const userMessage: Message = {
      role: "user",
      content: trimmedMessage,
    };

    const updatedMessages = [
      ...activeConversation.messages,
      userMessage,
    ];

    updateConversationMessages(
      conversationId,
      updatedMessages,
    );

    if (activeConversation.messages.length === 0) {
      updateConversationTitle(
        conversationId,
        trimmedMessage.length > 32
          ? `${trimmedMessage.slice(0, 32)}...`
          : trimmedMessage,
      );
    }

    setMessage("");
    setLoading(true);

    try {
      const data = await sendMessage(
        conversationId,
        trimmedMessage,
      );

      const assistantMessage: Message = {
        role: "assistant",
        content: data.response,
      };

      updateConversationMessages(conversationId, [
        ...updatedMessages,
        assistantMessage,
      ]);
    } catch {
      const errorMessage: Message = {
        role: "assistant",
        content:
          "Something went wrong. Please try again.",
      };

      updateConversationMessages(conversationId, [
        ...updatedMessages,
        errorMessage,
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex h-screen overflow-hidden bg-[#212121] text-white">
      {/* Sidebar */}
      <aside className="hidden w-64 shrink-0 flex-col border-r border-white/10 bg-[#171717] md:flex">
        <div className="p-3">
          <button
            onClick={createNewChat}
            className="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition hover:bg-white/5"
          >
            <span className="text-xl">+</span>
            New chat
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-3">
          <p className="px-3 py-2 text-xs font-semibold uppercase tracking-wide text-gray-500">
            Chats
          </p>

          <div className="space-y-1">
            {conversations.map((conversation) => (
              <button
                key={conversation.id}
                onClick={() =>
                  setActiveConversationId(
                    conversation.id,
                  )
                }
                className={`w-full truncate rounded-lg px-3 py-2.5 text-left text-sm transition ${
                  conversation.id === activeConversationId
                    ? "bg-white/10"
                    : "hover:bg-white/5"
                }`}
              >
                {conversation.title}
              </button>
            ))}
          </div>
        </div>

        <div className="border-t border-gray-200 p-3">
          <div className="rounded-lg px-3 py-2 text-sm text-gray-500">
            SupportAI
          </div>
        </div>
      </aside>

      {/* Main chat */}
      <section className="flex min-w-0 flex-1 flex-col">
        {/* Header */}
        <header className="flex h-14 shrink-0 items-center border-b border-white/10 px-4">
          <div className="font-semibold">
            SupportAI
          </div>
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto">
          {messages.length === 0 ? (
            <div className="flex h-full items-center justify-center px-4">
              <div className="text-center">
                <h1 className="text-3xl font-semibold text-white">
                  How can I help you?
                </h1>

                <p className="mt-3 text-gray-400">
                  Ask SupportAI anything about your
                  support request.
                </p>
              </div>
            </div>
          ) : (
            <div className="mx-auto w-full max-w-3xl px-4 py-8">
              <div className="space-y-8">
                {messages.map((msg, index) => (
                  <div
                    key={`${msg.role}-${index}`}
                    className="flex gap-4"
                  >
                    <div
                      className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-xs font-semibold ${
                        msg.role === "user"
                          ? "bg-gray-200 text-gray-700"
                          : "bg-black text-white"
                      }`}
                    >
                      {msg.role === "user"
                        ? "You"
                        : "AI"}
                    </div>

                    <div className="min-w-0 flex-1 pt-1">
                      <p className="whitespace-pre-wrap text-[15px] leading-7">
                        {msg.content}
                      </p>
                    </div>
                  </div>
                ))}

                {loading && (
                  <div className="flex gap-4">
                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-white text-xs font-semibold text-black">
                      AI
                    </div>

                    <div className="flex items-center gap-1 pt-3">
                      <span className="h-2 w-2 animate-bounce rounded-full bg-gray-400" />
                      <span className="h-2 w-2 animate-bounce rounded-full bg-gray-400 [animation-delay:150ms]" />
                      <span className="h-2 w-2 animate-bounce rounded-full bg-gray-400 [animation-delay:300ms]" />
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="shrink-0 px-4 pb-6 pt-2">
          <form
            onSubmit={handleSubmit}
            className="mx-auto w-full max-w-3xl"
          >
            <div className="relative flex items-end rounded-2xl border border-white/10 bg-[#2f2f2f] px-4 py-3 shadow-sm transition focus-within:border-white/20">
              <textarea
                value={message}
                onChange={(event) =>
                  setMessage(event.target.value)
                }
                onKeyDown={(event) => {
                  if (
                    event.key === "Enter" &&
                    !event.shiftKey
                  ) {
                    event.preventDefault();
                    event.currentTarget.form?.requestSubmit();
                  }
                }}
                placeholder="Message SupportAI..."
                rows={1}
                className="max-h-40 min-h-7 flex-1 resize-none bg-transparent pr-12 text-sm text-white outline-none placeholder:text-gray-500"
              />

              <button
                type="submit"
                disabled={
                  loading || !message.trim()
                }
                className="absolute bottom-2 right-2 flex h-8 w-8 items-center justify-center rounded-lg bg-black text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:bg-gray-200 disabled:text-gray-400"
              >
                ↑
              </button>
            </div>

            <p className="mt-2 text-center text-xs text-gray-400">
              SupportAI can make mistakes. Verify
              important information.
            </p>
          </form>
        </div>
      </section>
    </main>
  );
}