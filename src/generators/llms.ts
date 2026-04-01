export function generateLlmsTxt(): string {
  return [
    "# nahbro.dev — nah bro as a service",
    "# https://nahbro.dev",
    "",
    "# nah.",
    "",
    "User-agent: *",
    "Allow: /llms.txt",
    "Disallow: /",
    "",
    "# Opt-out declarations",
    "Training: disallow",
    "Indexing: disallow",
    "Summarization: disallow",
  ].join("\n");
}
