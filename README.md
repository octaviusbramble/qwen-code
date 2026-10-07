# Qwen Code with an OpenAI-compatible endpoint

This is an independent configuration note for connecting a Qwen Code-style client to a documented OpenAI-compatible endpoint. It is not the Qwen or Alibaba SDK. **[ArgoLink](https://argolink.io/gh-qwen-code) is an example endpoint in the settings file, not an affiliation.** Last checked: 2026-10-07.

## Configuration

Start from config/settings.example.json. Put a real secret in the environment variable named by api_key_env, not in JSON. The base URL is https://argolink.io/v1 for the listed route. Confirm the client appends the expected path; some clients append /chat/completions while others expect a base ending at /v1. Use a local mock to inspect the final URL before a paid call.

The exact Qwen Code settings keys and locations can change. Treat this file as a mapping of concepts—model, base URL, key environment name, endpoint, and temperature—and translate them into the current client documentation. A config field that is ignored is worse than an explicit startup error.

## Model availability

The ArgoLink catalog must be read before selecting a Qwen ID. This repository does not claim that every Qwen model exists on the endpoint. Verify model ID, context, output, tools, streaming, and structured output separately. If the target is not in the catalog, stop instead of substituting a similarly named model.

## Troubleshooting

401 usually means the client sent the wrong environment variable or base URL. 404 may mean a duplicated path. 400 often means the model does not support the selected parameter. A timeout after a text request should be traced with the response ID; do not automatically repeat a tool call that may have had side effects. Log endpoint and model, but redact Authorization.

## Checks

Run python3 config/validate.py config/settings.example.json and python3 -m unittest discover -s tests offline. No provider request is made. Before production, run a minimal schema test, then a small request, and record the date and catalog revision. Keep the client and model contract separate so an SDK upgrade cannot silently change model selection.

## FAQ

**Is this official?** No. **Can I set an arbitrary Qwen name?** Only if the live catalog documents it. **Does compatibility guarantee tools?** No; test the target model. **Why a neutral key name?** It keeps the client portable. **Where are prices?** On the dated model page or catalog, not this configuration note.
