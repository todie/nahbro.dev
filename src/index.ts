import { Hono } from "hono";
import { generateRobotsTxt } from "./generators/robots.js";
import { generateAiTxt } from "./generators/ai.js";
import { generateLlmsTxt } from "./generators/llms.js";

const app = new Hono();

// Root — explain the service
app.get("/", (c) => {
  return c.text(
    [
      "nahbro.dev — nah bro as a service",
      "",
      "tell LLMs no.",
      "",
      "ENDPOINTS:",
      "  GET /robots.txt          — robots.txt blocking all known AI crawlers",
      "  GET /ai.txt              — ai.txt (draft spec) disallowing all",
      "  GET /llms.txt            — llms.txt declaring opt-out",
      "  GET /generate            — all configs as JSON",
      "  GET /generate/robots     — robots.txt as plain text (alias)",
      "  GET /generate/ai         — ai.txt as plain text (alias)",
      "  GET /generate/llms       — llms.txt as plain text (alias)",
      "",
      "ADD TO YOUR SITE:",
      "  Drop the output of /generate/robots into your robots.txt",
      "  Drop /generate/ai into your ai.txt",
      "  Drop /generate/llms into your llms.txt",
      "",
      "source: https://github.com/todie/nahbro.dev",
    ].join("\n")
  );
});

// Serve the blocking files directly (meta: nahbro blocks bots on its own domain)
app.get("/robots.txt", (c) => {
  c.header("Content-Type", "text/plain; charset=utf-8");
  return c.text(generateRobotsTxt());
});

app.get("/ai.txt", (c) => {
  c.header("Content-Type", "text/plain; charset=utf-8");
  return c.text(generateAiTxt());
});

app.get("/llms.txt", (c) => {
  c.header("Content-Type", "text/plain; charset=utf-8");
  return c.text(generateLlmsTxt());
});

// Generation endpoints
app.get("/generate", (c) => {
  return c.json({
    "robots.txt": generateRobotsTxt(),
    "ai.txt": generateAiTxt(),
    "llms.txt": generateLlmsTxt(),
  });
});

app.get("/generate/robots", (c) => {
  c.header("Content-Type", "text/plain; charset=utf-8");
  return c.text(generateRobotsTxt());
});

app.get("/generate/ai", (c) => {
  c.header("Content-Type", "text/plain; charset=utf-8");
  return c.text(generateAiTxt());
});

app.get("/generate/llms", (c) => {
  c.header("Content-Type", "text/plain; charset=utf-8");
  return c.text(generateLlmsTxt());
});

export default {
  port: process.env.PORT ? parseInt(process.env.PORT) : 3000,
  fetch: app.fetch,
};
