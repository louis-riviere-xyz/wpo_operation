from datetime import date


class RuleDate:
    def __init__(self, items):
        self.min = date.fromisoformat(items['after'])
        self.max = date.fromisoformat(items['before'])

    def messages(self, req):
        msg = []
        if 'date' in req:
            if not self.min <= req['data'] <= self.max:
                msg.append((
                    'Invalid date',
                    f'{req["data"]} not between {self.min} and {self.max}'
                ))
        return msg

    def validate(self, req):
        if 'date' in req:
            if not self.min <= req['data'] <= self.max:
                return False
        return True


class RuleLevel:
    def __init__(self, items):
        if 'eq' in items:
            self.min = self.max = items['eq']
        else:
            self.min = items['gt']
            self.max = items['lt']

    def messages(self, req):
        msg = []
        if 'level' in req:
            if not self.min <= req['level'] <= self.max:
                if self.min == self.max:
                    msg.append((
                        'Invalid level',
                        f'{req["level"]} is not {self.max}'
                    ))
                else:
                    msg.append((
                        'Invalid level',
                        f'{req["level"]} is not between {self.min} and {self.max}'
                    ))
        return msg

    def validate(self, req):
        if 'level' in req:
            if not self.min <= req['level'] <= self.max:
                return False
        return True


class RuleMeteo:
    # TODO
    def __init__(self, items):
        pass

    def messages(self, req):
        msg = []
        return msg

    def validate(self, req):
        return True


class RuleOR:
    def __init__(self, rules):
        self.rules = rules

    def messages(self, req):
        msg = []
        for rule in self.rules:
            if m := rule.messages(req):
                msg.extend(m)
        return msg

    def validate(self, req):
        return any(rule.validate(req) for rule in self.rules)


class RuleAND:
    def __init__(self, rules):
        self.rules = rules

    def messages(self, req):
        msg = []
        for rule in self.rules:
            if m := rule.messages(req):
                msg.extend(m)
        return msg

    def validate(self, req):
        return all(rule.validate(req) for rule in self.rules)


class Restrictions:
    def get_rules(self, items):
        rules = []
        for i in items:
            for key, val in i.items():
                loader = getattr(self, f'load_{key[1:]}')
                rules.append(loader(val))
        return rules

    def load(self, items):
        self.rules = self.load_and(items)

    def validate(self, req):
        return self.rules.validate(req['arguments'])

    def messages(self, req):
        if self.validate(req):
            return []
        return self.rules.messages(req['arguments'])

    def load_level(self, items):
        return RuleLevel(items)

    def load_date(self, items):
        return RuleDate(items)

    def load_meteo(self, items):
        return RuleMeteo(items)

    def load_or(self, items):
        rules = self.get_rules(items)
        return RuleOR(rules)

    def load_and(self, items):
        rules = self.get_rules(items)
        return RuleAND(rules)


class Operation:
    def load(self, data):
        self.id = data['_id']
        self.name = data['name']
        self.priority = data['priority']['value']
        self.restrictions = Restrictions()
        self.restrictions.load(data['restrictions'])

    def accept(self):
        return {
            "operation_name": self.name,
            "status": "accepted",
            "priority": {"value": self.priority},
        }

    def deny(self, messages):
        return {
            "operation_name": self.name,
            "status": "denied",
            "reasons": dict(messages),
        }

    def validate(self, req):
        if msg := self.restrictions.messages(req):
            return self.deny(msg)
        else:
            return self.accept()
