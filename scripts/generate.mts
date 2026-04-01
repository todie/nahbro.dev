import { generateRobotsTxt } from "../src/generators/robots.js";
import { generateAiTxt } from "../src/generators/ai.js";
import { generateLlmsTxt } from "../src/generators/llms.js";
import { writeFileSync } from "fs";

const robotsTxt = generateRobotsTxt();
const aiTxt = generateAiTxt();
const llmsTxt = generateLlmsTxt();

writeFileSync("docs/robots.txt", robotsTxt);
writeFileSync("docs/ai.txt", aiTxt);
writeFileSync("docs/llms.txt", llmsTxt);
writeFileSync("docs/generate", JSON.stringify({ "robots.txt": robotsTxt, "ai.txt": aiTxt, "llms.txt": llmsTxt }, null, 2));
