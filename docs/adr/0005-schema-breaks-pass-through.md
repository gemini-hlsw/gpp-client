# Pass GPP schema breaks through to users

When GPP removes or renames a field, the client follows GPP and users see the break on their next upgrade. We keep no compatibility shims; release notes name what changed.

We rejected shims because GPP ships almost daily and shims would pile up as hand-maintained code against the maintenance goal. We rejected pinning users to a schema snapshot because an old client does not pin the server: GPP moves underneath it either way. The release contract in `docs/OVERVIEW.md` tells users to upgrade often.
