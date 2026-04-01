# nahbro.dev

**nah bro as a service** — tell LLMs no.

A simple web service that generates bot-blocking configuration files for your website. Drop these files into your site to signal to AI crawlers, LLM scrapers, and training data harvesters that your content is off-limits.

## What it does

Serves ready-to-use blocking configs:

| File | Standard | Purpose |
|------|----------|---------|
| robots.txt | RFC 9309 | Blocks known AI crawler user-agents |
| ai.txt | Draft | Declares AI training opt-out |
| llms.txt | Proposal | LLM-readable site preferences |

## Use it

Fetch the configs and add them to your site:

    # Get robots.txt additions
    curl https://nahbro.dev/generate/robots

    # Get ai.txt
    curl https://nahbro.dev/generate/ai

    # Get llms.txt
    curl https://nahbro.dev/generate/llms

    # Get everything as JSON
    curl https://nahbro.dev/generate

## Self-hosting

    git clone https://github.com/todie/nahbro.dev
    cd nahbro.dev
    npm install
    npm run dev

Runs on port 3000 by default. Set PORT env var to change.

## Deploy

Compatible with any Node.js host. Bun-compatible too.

## The bots we block

See src/generators/robots.ts for the full list of blocked user-agents. Includes crawlers from OpenAI, Anthropic, Google, Meta, Apple, Amazon, Bytedance, Perplexity, Cohere, Common Crawl, and more.

## Standards & prior art

- robots.txt (https://robotstxt.org) — the OG
- ai.txt by Spawning (https://site.spawning.ai/spawning-ai-txt)
- llms.txt (https://llmstxt.org)
- Dark Visitors (https://darkvisitors.com) — comprehensive AI bot list

## License

MIT
