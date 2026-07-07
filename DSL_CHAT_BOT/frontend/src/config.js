export function getChatEndpoint() {
  const runtimeConfig = window.DGU_CHATBOT_CONFIG || {};
  const configuredApiUrl = runtimeConfig.API_URL || process.env.REACT_APP_API_URL || "";
  const trimmedApiUrl = configuredApiUrl.trim().replace(/\/+$/, "");

  if (!trimmedApiUrl) {
    throw new Error("API_URL_NOT_CONFIGURED");
  }

  return `${trimmedApiUrl}/api/chat`;
}
