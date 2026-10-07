# Qwen Code with an OpenAI-compatible endpoint

This is an independent configuration and verification note for connecting the current Qwen Code CLI to an OpenAI-compatible model provider. It is not the Qwen or Alibaba SDK. **[ArgoLink](https://argolink.io/gh-qwen-code) is an example endpoint, not an affiliation.** Checked 2026-10-07.

## Current Qwen Code configuration contract

Qwen Code's current documentation uses `~/.qwen/settings.json` and the `modelProviders` object. For an OpenAI-compatible route, the provider key is `openai`; each model entry declares `id`, `name`, `baseUrl`, and `envKey`. `wireApi` is `chat-completions` or `responses`; omit it only when the provider's default is the contract you actually want. `security.auth.selectedType` selects `openai`, and `model.name` selects an ID from the configured list.

[`config/settings.example.json`](config/settings.example.json) is a safe, key-free example for the live ArgoLink catalog:

```json
{
  "modelProviders": {
    "openai": [{
      "id": "gpt-6-sol",
      "name": "GPT-6 Sol via ArgoLink",
      "baseUrl": "https://argolink.io/v1",
      "envKey": "OPENAI_API_KEY",
      "wireApi": "responses"
    }]
  },
  "security": {"auth": {"selectedType": "openai"}},
  "model": {"name": "gpt-6-sol"}
}
```

`gpt-6-sol` is the model ID verified in the 2026-10-07 ArgoLink catalog, with a Responses route. Qwen Code is the client here; the model does not need to be a Qwen model. If the live catalog does not contain a desired Qwen model ID, stop instead of substituting a similarly named model.

## Secret and environment setup

Prefer the shell or `~/.qwen/.env`; Qwen Code's documented priority is CLI flags, process environment, `.env`, then a settings-file `env` fallback. The example uses only the variable name:

```bash
export OPENAI_API_KEY='replace-with-a-development-key'
qwen
```

For a provider that uses an environment-only setup, the documented variables are `OPENAI_API_KEY`, `OPENAI_BASE_URL`, and `OPENAI_MODEL` (with `QWEN_MODEL` as an alias). The `modelProviders` form is preferable when a project needs an explicit `wireApi`, timeout, or multiple model entries. Never put a real key in JSON, YAML, shell history committed to a repository, or an issue.

## Verify without a billable request

```bash
python3 config/validate.py config/settings.example.json
python3 -m unittest discover -s tests -v
```

Then inspect the client configuration and use `/doctor` inside Qwen Code. A local mock can assert whether the client sends `/v1/responses` or `/v1/chat/completions`, the selected model ID, and the expected Authorization header without contacting a provider. The first approved canary should be small, have an explicit budget, and retain its response ID.

## Model and endpoint checks

Read `GET https://argolink.io/v1/models` and the model page on the same date as configuration. Verify model ID, endpoint family, context/output limits, reasoning effort names, tools, streaming, image input, usage fields, and price unit separately. `gpt-6-sol` currently uses `/v1/responses`; a chat-only sample is not a valid substitute for a Responses tool loop. The model page wins over this README if a field changes.

## Troubleshooting

- **401:** the process did not receive the variable named by `envKey`, or the key belongs to another base URL.
- **404:** the client may have appended `/chat/completions` to a base that already includes a path, or the selected model route is absent.
- **400:** inspect `wireApi`, model ID, reasoning fields, and unsupported sampling parameters.
- **No model in `/model`:** the provider key is not `openai`, `security.auth.selectedType` is wrong, or `model.name` does not match an entry.
- **Timeout:** keep the response ID if one exists; do not automatically repeat a tool call that may have had side effects.

## Workflow and sources

[`workflow/plan.yaml`](workflow/plan.yaml) records the safe sequence. Qwen Code's current primary docs: [authentication](https://github.com/QwenLM/qwen-code/blob/main/docs/users/configuration/auth.md), [settings](https://github.com/QwenLM/qwen-code/blob/main/docs/users/configuration/settings.md), and [model providers](https://github.com/QwenLM/qwen-code/blob/main/docs/users/configuration/model-providers.md). ArgoLink sources: [model list](https://argolink.io/v1/models) and [model pages](https://argolink.io/en/models).
