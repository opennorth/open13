from billy.scrape.actions import Rule, BaseCategorizer


# These are regex patterns that map to action categories.
_categorizer_rules = (
    # Rule('Amended', 'amendment:passed'),
    # Rule('Committee', 'committee:passed'),
    # Rule('Reading', 'bill:reading:1'),
    # #Rule('Report', 'bill:'),
    # #Rule('Royal Assent'),
    # Rule('Second Reading', 'bill:reading:2'),
    # Rule('Third Reading', 'bill:reading:3'),
    )


class Categorizer(BaseCategorizer):
    rules = _categorizer_rules
