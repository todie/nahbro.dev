const AI_BOTS = [
  // OpenAI
  "GPTBot",
  "ChatGPT-User",
  "OAI-SearchBot",
  // Anthropic
  "ClaudeBot",
  "Claude-Web",
  "anthropic-ai",
  // Google AI
  "Google-Extended",
  // Meta
  "meta-externalagent",
  "FacebookBot",
  // Apple
  "Applebot-Extended",
  // Amazon
  "Amazonbot",
  // Common Crawl / training data
  "CCBot",
  "DataForSeoBot",
  // Bytedance
  "Bytespider",
  // Perplexity
  "PerplexityBot",
  // Cohere
  "cohere-ai",
  // Diffbot
  "Diffbot",
  "ai2-unsafe-agent",
  // Scrapers commonly used for AI training
  "ImagesiftBot",
  "omgili",
  "omgilibot",
  "Meltwater",
  // Misc AI agents
  "YouBot",
  "Timpibot",
  "PetalBot",
  "Kangaroo Bot",
  "SemrushBot-OCOB",
];

export function generateRobotsTxt(): string {
  const lines: string[] = [
    "# nahbro.dev — nah bro as a service",
    "# https://nahbro.dev",
    "",
    "# nah.",
    "",
    ...AI_BOTS.flatMap((bot) => [`User-agent: ${bot}`, "Disallow: /", ""]),
    "User-agent: *",
    "Allow: /",
  ];
  return lines.join("\n");
}
