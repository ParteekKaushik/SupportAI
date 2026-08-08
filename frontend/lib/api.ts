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