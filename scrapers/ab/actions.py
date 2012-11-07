from billy.scrape.actions import Rule, BaseCategorizer


# These are regex patterns that map to action categories.
_categorizer_rules = (
    Rule(['Third Reading.+?passed'], ['bill:reading:3', 'bill:failed']),
    Rule(['Second Reading.+?passed'], ['bill:reading:2']),
    Rule(['First Reading'], ['bill:reading:1']),
    )


class Categorizer(BaseCategorizer):
    rules = _categorizer_rules
