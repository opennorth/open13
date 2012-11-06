from billy.scrape.actions import Rule, BaseCategorizer


# These are regex patterns that map to action categories.
_categorizer_rules = (
    )


class Categorizer(BaseCategorizer):
    rules = _categorizer_rules
