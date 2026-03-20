"""Structural search engine for UD treebank data.

Matches tokens based on structural constraints: properties of the target token,
its head, its dependents, and negated dependent patterns.
"""

from __future__ import annotations

from typing import Any


def parse_feats(feats_str: str) -> dict[str, str]:
    """Parse a UD feats string into a dict.

    Examples:
        >>> parse_feats("Case=Nom|Number=Sing")
        {'Case': 'Nom', 'Number': 'Sing'}
        >>> parse_feats("_")
        {}
    """
    if not feats_str or feats_str == "_":
        return {}
    result: dict[str, str] = {}
    for pair in feats_str.split("|"):
        if "=" in pair:
            key, _, value = pair.partition("=")
            result[key] = value
        else:
            result[pair] = ""
    return result


def _is_regular_token(id_f: str) -> bool:
    """Return True if the token is a regular word (not MWT or empty node)."""
    return "-" not in id_f and "." not in id_f


def _matches_node_constraint(
    token: dict[str, Any],
    constraint: dict[str, Any],
    parsed_feats: dict[str, str] | None = None,
) -> bool:
    """Check whether a token satisfies a node constraint.

    Args:
        token: A wordline dict with keys id_f, form, lemma, upos, etc.
        constraint: A constraint dict with optional keys: upos, feats, form, lemma.
        parsed_feats: Pre-parsed feats for the token; computed if not provided.

    Returns:
        True if all specified constraints are satisfied.
    """
    # UPOS check: token's upos must be in the allowed list
    upos_list = constraint.get("upos")
    if upos_list and token.get("upos", "_") not in upos_list:
        return False

    # Form check (case-insensitive exact match)
    form = constraint.get("form")
    if form is not None and token.get("form", "").lower() != form.lower():
        return False

    # Lemma check (case-insensitive exact match)
    lemma = constraint.get("lemma")
    if lemma is not None and token.get("lemma", "").lower() != lemma.lower():
        return False

    # Feature constraints: each required feature key must have a matching value
    feat_constraints = constraint.get("feats")
    if feat_constraints:
        if parsed_feats is None:
            parsed_feats = parse_feats(token.get("feats", "_"))
        for feat_key, allowed_values in feat_constraints.items():
            token_value = parsed_feats.get(feat_key)
            if token_value is None:
                return False
            if allowed_values and token_value not in allowed_values:
                return False

    return True


def _matches_relation_constraint(
    token: dict[str, Any],
    constraint: dict[str, Any],
    parsed_feats: dict[str, str] | None = None,
) -> bool:
    """Check whether a token satisfies a relation constraint (node + deprel).

    The deprel is checked on the token itself (the dependent side of the relation).
    """
    # Deprel check
    deprel_list = constraint.get("deprel")
    if deprel_list and token.get("deprel", "_") not in deprel_list:
        return False

    return _matches_node_constraint(token, constraint, parsed_feats)


def match_structural(
    query: dict[str, Any],
    wordlines: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Find tokens matching a structural query within a single sentence.

    Args:
        query: A structural query dict with keys: target, head_constraint,
            dependent_constraints, negated_dependents.
        wordlines: List of wordline dicts (one sentence). Each dict has keys:
            id_f, form, lemma, upos, xpos, feats, head, deprel, deps, misc.

    Returns:
        List of wordline dicts for target tokens that match all constraints.
    """
    # Filter to regular tokens only
    regular = [wl for wl in wordlines if _is_regular_token(wl["id_f"])]

    # Build lookup structures
    by_id: dict[str, dict[str, Any]] = {wl["id_f"]: wl for wl in regular}
    # Map head_id -> list of dependent tokens
    dependents_of: dict[str, list[dict[str, Any]]] = {}
    for wl in regular:
        head_id = wl.get("head", "0")
        dependents_of.setdefault(head_id, []).append(wl)

    # Pre-parse feats for all tokens
    feats_cache: dict[str, dict[str, str]] = {
        wl["id_f"]: parse_feats(wl.get("feats", "_")) for wl in regular
    }

    target_constraint = query.get("target", {})
    head_constraint = query.get("head_constraint")
    dep_constraints = query.get("dependent_constraints") or []
    neg_constraints = query.get("negated_dependents") or []

    matched: list[dict[str, Any]] = []

    for token in regular:
        tid = token["id_f"]

        # 1. Check target constraints
        if not _matches_node_constraint(token, target_constraint, feats_cache[tid]):
            continue

        # 2. Check head constraint
        if head_constraint:
            head_id = token.get("head", "0")
            if head_id == "0":
                # Root token has no head to match against
                continue
            head_token = by_id.get(head_id)
            if head_token is None:
                continue

            # The deprel in head_constraint refers to the relation label on
            # the TARGET token (the arc from head to target carries target's deprel)
            deprel_list = head_constraint.get("deprel")
            if deprel_list and token.get("deprel", "_") not in deprel_list:
                continue

            # Check node constraints (upos, feats, form, lemma) on the head
            if not _matches_node_constraint(
                head_token, head_constraint, feats_cache.get(head_id)
            ):
                continue

        # 3. Check dependent constraints (each must be satisfied by at least one dep)
        deps_of_target = dependents_of.get(tid, [])
        if dep_constraints:
            all_dep_ok = True
            for dep_c in dep_constraints:
                found = any(
                    _matches_relation_constraint(dep, dep_c, feats_cache.get(dep["id_f"]))
                    for dep in deps_of_target
                )
                if not found:
                    all_dep_ok = False
                    break
            if not all_dep_ok:
                continue

        # 4. Check negated dependents (none of the deps may match)
        if neg_constraints:
            any_neg_match = False
            for neg_c in neg_constraints:
                found = any(
                    _matches_relation_constraint(dep, neg_c, feats_cache.get(dep["id_f"]))
                    for dep in deps_of_target
                )
                if found:
                    any_neg_match = True
                    break
            if any_neg_match:
                continue

        matched.append(token)

    return matched
