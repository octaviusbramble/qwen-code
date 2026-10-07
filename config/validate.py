"""Validate a Qwen Code model-provider settings example without network access."""
from __future__ import annotations

import argparse
import json
import pathlib
import re

SUPPORTED_WIRE_APIS = {"chat-completions", "responses"}


def validate(path: pathlib.Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read settings: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("settings root must be an object")
    providers = data.get("modelProviders", {}).get("openai")
    if not isinstance(providers, list) or not providers:
        raise ValueError("modelProviders.openai must contain at least one model")
    selected = data.get("security", {}).get("auth", {}).get("selectedType")
    if selected != "openai":
        raise ValueError("security.auth.selectedType must be openai")
    selected_name = data.get("model", {}).get("name")
    ids = set()
    for provider in providers:
        if not isinstance(provider, dict):
            raise ValueError("each model provider must be an object")
        for key in ("id", "name", "baseUrl", "envKey", "wireApi"):
            if not isinstance(provider.get(key), str) or not provider[key]:
                raise ValueError(f"provider.{key} is required")
        if provider["id"] in ids:
            raise ValueError(f"duplicate provider model id: {provider['id']}")
        ids.add(provider["id"])
        if not re.fullmatch(r"https://[^/\s]+(?:/.*)?", provider["baseUrl"]):
            raise ValueError("provider.baseUrl must be an absolute HTTPS URL")
        if provider["wireApi"] not in SUPPORTED_WIRE_APIS:
            raise ValueError("wireApi must be chat-completions or responses")
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*", provider["envKey"]):
            raise ValueError("envKey must be an uppercase environment variable name")
        generation = provider.get("generationConfig", {})
        if not isinstance(generation, dict) or generation.get("maxRetries", 0) < 0:
            raise ValueError("generationConfig.maxRetries must be non-negative")
    if selected_name not in ids:
        raise ValueError("model.name must match a configured provider model id")
    if "env" in data and any("KEY" in key and isinstance(value, str) and value.startswith("sk-") for key, value in data["env"].items()):
        raise ValueError("settings example must not contain a real API key")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Qwen Code settings.json offline")
    parser.add_argument("path", type=pathlib.Path)
    args = parser.parse_args()
    validate(args.path)
    print(f"valid: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
