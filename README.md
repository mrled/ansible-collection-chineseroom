# Ansible Collection - mrled.chineseroom

Run LLM agents without permission checks.

Currently this contains a single role: [`chineseroom`](./roles/chineseroom),
which configures a Fedora 42 install with a restricted agent user.

[Published to Ansible Galaxy](https://galaxy.ansible.com/ui/repo/published/mrled/chineseroom/).

## Development

Symlink the role to an Ansible site and it'll work directly.

Build the collection for publishing with:

```sh
ansible-galaxy collection build
```

### Releasing

GitHub Actions handles publishing to Ansible Galaxy based on version tags.

Create and push a version tag with:

```sh
git tag v1.2.3
git push origin master --tags
```
