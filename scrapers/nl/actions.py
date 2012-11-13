from billy.scrape.actions import Rule, BaseCategorizer


# These are regex patterns that map to action categories.
_categorizer_rules = (
    Rule('First Reading', 'bill:reading:1'),
    Rule('Second Reading', 'bill:reading:2'),
    Rule('Committee', 'committee:passed'),
    Rule('Amendments', 'amendment:passed'),
    Rule('Third Reading', 'bill:reading:3'),
    )


class Categorizer(BaseCategorizer):
    rules = _categorizer_rules
