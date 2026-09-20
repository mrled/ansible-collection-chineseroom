# Ansible Collection - mrled.chineseroom

Run LLM agents without permission checks.

<!--Use absolute links here because the same readme is shown on Ansible Galaxy and GitHub-->

Currently this contains a single role:
[`chineseroom`](https://github.com/mrled/ansible-collection-chineseroom/tree/master/roles/chineseroom),
which configures a Fedora 42 install with a restricted agent user.
That role has its own readme, which lists features and describes how to use it.

* [Ansible Galaxy](https://galaxy.ansible.com/ui/repo/published/mrled/chineseroom/)
* [GitHub](https://github.com/mrled/ansible-collection-chineseroom)
* [Announcement blog post](https://me.micahrl.com/blog/claude-code-chinese-room/).

## Development

Symlink the role to an Ansible site and it'll work directly.

Build the collection for publishing with:

```sh
ansible-galaxy collection build
```

### Releasing

GitHub Actions handles publishing to Ansible Galaxy based on version tags,
but Ansible Galaxy knows only about the contents of `galaxy.yml`.
`./release.py` handles both.

```sh
# Bump the major version, e.g. 1.2.3 -> 2.0.0
./release.py major

# Bump the minor version, e.g. 1.2.3 -> 1.3.0
./release.py minor

# Bump the patch version, e.g. 1.2.3 -> 1.2.4
./release.py patch

# Release a specific version
./release.py 2.0.1
```
