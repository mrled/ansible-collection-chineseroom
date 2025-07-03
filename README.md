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

GitHub Actions handles publishing to Ansible Galaxy based on version tags.

Create and push a version tag with:

```sh
git tag v1.2.3
git push origin master --tags
```
