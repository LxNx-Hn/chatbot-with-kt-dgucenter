const fs = require("fs");
const path = require("path");

const outputPath = path.join(__dirname, "..", "build", "config.js");
const configuredApiUrl = (process.env.REACT_APP_API_URL || process.env.API_URL || "").trim();
const requireApiUrl = process.env.REQUIRE_RUNTIME_API_URL === "true";

if (requireApiUrl && !configuredApiUrl) {
  throw new Error("REACT_APP_API_URL or API_URL is required to write runtime config.");
}

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(
  outputPath,
  `window.DGU_CHATBOT_CONFIG = ${JSON.stringify({ API_URL: configuredApiUrl }, null, 2)};\n`,
  "utf8"
);

console.log(`Wrote runtime config to ${outputPath}`);
