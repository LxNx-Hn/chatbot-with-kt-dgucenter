import requests
from config.constants import MODEL_NAME
from config.settings import (
    MODEL_PROVIDER,
    NVIDIA_API_KEY,
    NIM_BASE_URL,
    NIM_MODEL,
    NIM_TIMEOUT_SECONDS,
)


class MissingModelConfigurationError(RuntimeError):
    pass


class LocalLLMProvider:
    def __init__(self):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

        self.model_name = MODEL_NAME
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.llm = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
            trust_remote_code=True,
        )
        self.gen_config = GenerationConfig.from_pretrained(self.model_name)

    def generate_response(self, messages, max_new_tokens=512, do_sample=True):
        input_ids = self.tokenizer.apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
        ).to(self.llm.device)
        output = self.llm.generate(
            input_ids,
            generation_config=self.gen_config,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
        )
        response = self.tokenizer.decode(output[0][input_ids.shape[-1] :], skip_special_tokens=True)
        return response.strip()


class NimLLMProvider:
    def __init__(self):
        self.base_url = NIM_BASE_URL
        self.model = NIM_MODEL
        self.api_key = NVIDIA_API_KEY
        self.timeout = NIM_TIMEOUT_SECONDS

    def generate_response(self, messages, max_new_tokens=512, do_sample=True):
        if not self.api_key:
            raise MissingModelConfigurationError(
                "NVIDIA_API_KEY 또는 NIM_API_KEY 환경변수가 설정되어 있지 않습니다."
            )

        temperature = 0.7 if do_sample else 0.0
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": messages,
                "max_tokens": max_new_tokens,
                "temperature": temperature,
                "stream": False,
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        choices = data.get("choices") or []
        if not choices:
            raise RuntimeError("NIM 응답에 choices가 없습니다.")
        message = choices[0].get("message") or {}
        content = message.get("content", "")
        return content.strip()


class LLMModel:
    def __init__(self):
        self.provider_name = MODEL_PROVIDER
        if self.provider_name == "nim":
            self.provider = NimLLMProvider()
        elif self.provider_name == "local":
            self.provider = LocalLLMProvider()
        else:
            raise MissingModelConfigurationError(
                f"지원하지 않는 MODEL_PROVIDER 값입니다: {self.provider_name}"
            )

    def generate_response(self, messages, max_new_tokens=512, do_sample=True):
        return self.provider.generate_response(
            messages,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
        )


llm_instance = LLMModel()
