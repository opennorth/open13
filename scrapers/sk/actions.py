from billy.scrape.actions import Rule, BaseCategorizer


# These are regex patterns that map to action categories.
_categorizer_rules = (
    Rule('First Reading', 'bill:reading:1'),
    Rule('Committee', 'committee:referred'),
    Rule('Second Reading', 'bill:reading:2'),
    Rule('Committee', 'committee:passed'),
    Rule('Amend Date', 'amendment:passed'),
    Rule('Third Reading', 'bill:reading:3'),
    Rule('Royal Assent', 'governor:approved'),
    )


class Categorizer(BaseCategorizer):
    rules = _categorizer_rules
