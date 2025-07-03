# Ansible Collection - mrled.chineseroom

A role for a Fedora 42 machine to let agents run wild.

Too responsible to run Claude Code in YOLO mode (`--dangerously-skip-permissions`) on your workstation?
Deploy Fedora to a VM instead and configure it with this role.

## Threat model

Manage the [lethal trifecta for AI agents](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/):

- Allow external communication (it can use the Internet)
- Give it access to untrusted content (the Internet, random corpus, or anything else you want)
- But don't give it private data

Run the agent on a separate machine without API keys, passwords, tax returns, and nudes.

## Prerequisites

- Install Fedora 42
  - During the install, set up a user for yourself that will have sudo,
    but don't set up the restricted user; the Ansible playbook will do that
- Configure passwordless ssh keys for Ansible to log in to
- A domain (or subdomain) with Route53 DNS hosting
- Install AWS credentials to `/root/.aws/credentials` with permissions required to use Certbot with the route53 plugin

## Role Variables

See [defaults/main.yml](./defaults/main.yml) for configuration variables.

## Features

- An agent user without sudo access
- HTTP servers on subdomains

### Agent user without sudo

- You'll ssh to this user, and you can edit code, run the code, run tests, etc yourself.
- You'll also launch `claude --dangerously-skip-permissions` and have it do these things,
  as well as run tools for you across codebases,
  browse the web,
  use Playwright MCP,
  etc.

### HTTP servers on subdomains

A secure way for the agent user to run an HTTP server on a localhost port,
and be proxied through a webserver listening on a real subdomain you control with a real HTTPS certificate.

- You can see what it's working on from your workstation
- You can check out multiple copies of the same repo and have `site1.chineseroom.example.com`, `site2.chineseroom.example.com` etc
- The agent can also look at what's running on those subdomains with Playwright MCP

How it works:

- Get Let's Encrypt certificates for a domain and all subdomains to dedicate to the Chinese Room
  e.g. `chineseroom.example.com`
    - Get the certs as root, and copy them to nginx config
    - Don't give the agent DNS API keys
- The restricted user creates subdomain mappings by editing `~/domainmap.txt`, for example:
  ```text
  test 8080
  yourapp 3000
  ```
  - The restricted user runs `sudo /usr/local/bin/regen-nginx-mappings.sh`
    (it is only allowed to sudo this command)
  - The script creates an nginx config with the mappings and makes them available on the domain you have:
    - `https://test.chineseroom.example.com` is proxied to `http://localhost:8080`
    - `https://yourapp.chineseroom.example.com` is proxied to `http://localhost:3000`

## Notes

### Don't give it permissions to push to your repos

Instead, create bare repos, push your code to them from a trusted workstation,
and pull code from them to review on a trusted workstation.

In detail:

- Create bare repos in somewhere like `~/repos/` as the restricted user
- Create a `chineseroom` remote pointing to these bare repos
- Check out and run code on your regular workstation as normal
- Push to the `chineseroom` remote and let the agent clone and push to there
- More sandboxed than a Docker container with the repo mounted as a volume,
  because it prevents the agent from adding scripts to git hooks or smudge filters that could obscure diffs
- Pull code from the `chineseroom` remote safely, review it on your workstation as normal,
  and run it when satisfied

### Playwright MCP and Claude

The default instructions assume Chrome is installed.
Chrome is only installable on x86_64, and this role is meant to work on aarch64 as well, so we don't install it.
Enable Playwright MCP and tell it to use Firefox instead:

```sh
claude mcp add playwright npx -- '@playwright/mcp@latest' --browser firefox
```

The role can't do this for you because it must be done separately in each Claude workspace.
