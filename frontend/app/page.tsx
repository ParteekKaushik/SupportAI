"use client";

import { useEffect, useState } from "react";

import { getHealth } from "@/lib/api";

type HealthResponse = {
  status: string;
  service: string;
};

export default function Home() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function checkBackend() {
      try {
        const data = await getHealth();
        setHealth(data);
      } catch (error) {
        setError("Backend connection failed");
      }
    }

    checkBackend();
  }, []);

  return (
    <main className="flex min-h-screen items-center justify-center">
      <div className="text-center">
        <h1 className="text-3xl font-bold">
          SupportAI
        </h1>

        {health && (
          <p className="mt-4">
            Backend: {health.status}
          </p>
        )}

        {error && (
          <p className="mt-4">
            {error}
          </p>
        )}
      </div>
    </main>
  );
}