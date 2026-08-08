const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function getHealth() {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/health`,
  );

  if (!response.ok) {
    throw new Error("Failed to connect to SupportAI backend");
  }

  return response.json();
}

export type ChatResponse = {
  response: string;
};

export async function sendMessage(
  message: string,
): Promise<ChatResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/chat`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message,
      }),
    },
  );

  if (!response.ok) {
    throw new Error("Failed to send message");
  }

  return response.json();
}