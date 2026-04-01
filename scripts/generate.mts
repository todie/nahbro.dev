import { generateRobotsTxt } from "./src/generators/robots.js";
import { generateAiTxt } from "./src/generators/ai.js";
import { generateLlmsTxt } from "./src/generators/llms.js";
import { writeFileSync } from "fs";

writeFileSync("docs/robots.txt", generateRobotsTxt());
writeFileSync("docs/ai.txt", generateAiTxt());
writeFileSync("docs/llms.txt", generateLlmsTxt());
writeFileSync("docs/aristocrats", "the aristocrats.");
console.log("done");
