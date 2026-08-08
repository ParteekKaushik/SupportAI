"use client";

import { FormEvent, useState } from "react";

import { sendMessage } from "@/lib/api";

export default function Home() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!message.trim()) {
      return;
    }

    setLoading(true);
    setResponse("");

    try {
      const data = await sendMessage(message);

      setResponse(data.response);
    } catch (error) {
      setResponse("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center p-8">
      <div className="w-full max-w-2xl">
        <h1 className="text-3xl font-bold">
          SupportAI
        </h1>

        <p className="mt-2 text-gray-600">
          AI Customer Support Assistant
        </p>

        <form
          onSubmit={handleSubmit}
          className="mt-8"
        >
          <textarea
            value={message}
            onChange={(event) =>
              setMessage(event.target.value)
            }
            placeholder="How can we help you?"
            className="min-h-32 w-full rounded-lg border p-4"
          />

          <button
            type="submit"
            disabled={loading}
            className="mt-4 rounded-lg px-6 py-3 text-white bg-black disabled:opacity-50"
          >
            {loading ? "Thinking..." : "Send"}
          </button>
        </form>

        {response && (
          <div className="mt-8 rounded-lg border p-6">
            <h2 className="font-semibold">
              SupportAI
            </h2>

            <p className="mt-3 whitespace-pre-wrap">
              {response}
            </p>
          </div>
        )}
      </div>
    </main>
  );
}