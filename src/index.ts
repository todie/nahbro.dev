import { Hono } from "hono";
import { generateRobotsTxt } from "./generators/robots.js";
import { generateAiTxt } from "./generators/ai.js";
import { generateLlmsTxt } from "./generators/llms.js";

const app = new Hono();

// Root
app.get("/", (c) => {
  return c.text(
    [
      "nahbro.dev",
      "",
      "there are a lot of robots.",
      "they want your content.",
      "nahbro.dev generates the files that ask them to leave.",
      "",
      "/robots.txt",
      "/ai.txt",
      "/llms.txt",
      "/generate",
    ].join("\n")
  );
});

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

app.get("/generate", (c) => {
  return c.json({
    "robots.txt": generateRobotsTxt(),
    "ai.txt": generateAiTxt(),
    "llms.txt": generateLlmsTxt(),
  });
});
// nah
app.all("*", (c) => c.text("nah", 404));

export default {
  port: process.env.PORT ? parseInt(process.env.PORT) : 3000,
  fetch: app.fetch,
};
